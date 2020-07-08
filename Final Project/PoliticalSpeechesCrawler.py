import urllib2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import time
import os

def pdf_from_url_to_txt(url):
    # Turning URL of PDF to text
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Open the url provided as an argument to the function and read the content
    f = urllib2.urlopen(urllib2.Request(url)).read()
    # Cast to StringIO object
    fp = StringIO(f)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp,pagenos,maxpages=maxpages,password=password,caching=caching,check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

def SpeechesFolder():
    # Creation of the Main Folder
    print "Creating the main folder"
    folderPath = "C:\\" + os.path.join(os.environ["HOMEPATH"], "Desktop\PoliticalSpeeches")
    if not os.path.exists(folderPath):
        os.mkdir(folderPath)
    ObamaSpeeches()
    BushSpeeches()
    ClintonSpeeches()


def ObamaSpeeches():
    #Obama Speeches
    print("Starts Obama's Speeches\n")
    obamaURL = "http://www.americanrhetoric.com/barackobamaspeeches.htm"
    try:
        page = urllib2.urlopen(obamaURL)
    except:
        print "Problem to connect to the Speeches Site"
        return False
    page_content = page.read()
    tempLinks = str(page_content).split("href=\"")
    obamaLstLinks = []
    print "Collecting the relevant Speeches"
    # Getting the links of the PDF speeches
    for link in tempLinks:
        if ("speeches/" in link) and ("PDFFiles" in link):
            obamaLstLinks.append(link.split(".pdf")[0] + ".pdf")
    countObama = 1
    # Creation of Bush's Folder
    obamaPath = "C:\\" + os.path.join(os.environ["HOMEPATH"], "Desktop\PoliticalSpeeches\Obama_Speeches")
    if not os.path.exists(obamaPath):
        os.mkdir(obamaPath)
    obamaLength = str(len(obamaLstLinks))
    # Scanning all the speeches - PDF
    print "Starts The Scan"
    for i in obamaLstLinks:
        newURL = "http://www.americanrhetoric.com/" + i
        print 'URL Number ' + str(countObama) + ' of ' + obamaLength + '. URL: ' + newURL
        try:
            tempText = pdf_from_url_to_txt(newURL)
            file_name = "Speech Number " + str(countObama) + ".txt"
            open(obamaPath + '\\' + file_name, "w")
            # Cleaning Data
            text = str(tempText).replace('', '').replace('AAmmeerriiccaannRRhheettoorriicc..ccoomm', '').replace(
                'AmericanRhetoric.com', '').replace(' \n', '').split('\n')
            eigthLine = 0
            # Writing the Speech to txt file
            for line in text:
                # Ignoring the meta data
                if (eigthLine < 8):
                    eigthLine += 1
                    continue
                if (len(line) < 1) or ('Page ' in line) or (('from' in line) and ('audio' in line)):
                    continue
                with open(obamaPath + '\\' + file_name, "a") as fid:
                    fid.write(line + "\n")
            countObama += 1
            # Don't overload the server
            time.sleep(2)
        except:
            continue

def BushSpeeches():
    # Bush Speeches
    print("\nStarts Bush's Speeches\n")
    bushURL = "http://www.americanrhetoric.com/gwbushspeeches.htm"
    try:
        page = urllib2.urlopen(bushURL)
    except:
        print "Problem to connect to the Speeches Site"
        return False
    page_content = page.read()
    tempLinks = str(page_content).split("href=\"")
    bushLstLinks = []
    print "Collecting The Relevant Speeches"
    # Getting the links of the PDF speeches
    for link in tempLinks:
        if ("speeches/" in link) and ("PDFFiles" in link):
            bushLstLinks.append(link.split(".pdf")[0] + ".pdf")
    countBush = 1
    # Creation of Bush's Folder
    bushPath = "C:\\" + os.path.join(os.environ["HOMEPATH"], "Desktop\PoliticalSpeeches\Bush_Speeches")
    if not os.path.exists(bushPath):
        os.mkdir(bushPath)
    bushLength = str(len(bushLstLinks))
    # Scanning all the speeches - PDF
    print "Starts The Scan"
    for i in bushLstLinks:
        newURL = "http://www.americanrhetoric.com/" + i
        print 'URL Number ' + str(countBush) + ' of ' + bushLength + '. URL: ' + newURL
        try:
            tempText = pdf_from_url_to_txt(newURL)
            file_name = "Speech Number " + str(countBush) + ".txt"
            open(bushPath + '\\' + file_name, "w")
            # Cleaning Data
            text = str(tempText).replace('', '').replace('AAmmeerriiccaannRRhheettoorriicc..ccoomm', '').replace(
                'AmericanRhetoric.com', '').replace(' \n', '').split('\n')
            eigthLine = 0
            # Writing the Speech to txt file
            for line in text:
                # Ignoring the meta data
                if (eigthLine < 8):
                    eigthLine += 1
                    continue
                if (len(line) < 1) or ('Page ' in line) or (('from' in line) and ('audio' in line)) or (('rights' in line) and ('reserved' in line)) or (('Property' in line) and ('of' in line)):
                    continue
                with open(bushPath + '\\' + file_name, "a") as fid:
                    fid.write(line + "\n")
            countBush += 1
            # Don't overload the server
            time.sleep(2)
        except:
            continue

def ClintonSpeeches():
    # Clinton Speeches
    print("\nStarts Clinton's Speeches\n")
    # Creation of Clinton's Folder
    clintonPath = "C:\\" + os.path.join(os.environ["HOMEPATH"], "Desktop\PoliticalSpeeches\Clinton_Speeches")
    if not os.path.exists(clintonPath):
        os.mkdir(clintonPath)
    url = "http://www.presidency.ucsb.edu/ws/index.php?pid="
    # The relevant Speeches
    print "Collecting The Relevant Speeches"
    speechesID = ['940','947','952','1012','1043','1121','1193','1200','1211','1220','1228','1235','1254','1259','1265','1267','1268','1271','1272','1276','1286','1290','1292','1295','25548','25549','25958','45997','45998','46009','46086','46109','46120','46131','46164','46166','46366','46317','46320','46321','46328','46348','46352','46353','46378','46444','46466','46477','46538','46539','46542','46543','46548','46550','46551','46600','46644','46711','46755','46766','46799','46811','46822','46877','46944','46988','46999','47010','47188','47210','47243','48952','48953','48955','48957','51423','51434','51579','61530','62409','62463','65345','77817','85226','85227','85229','118046']
    speechesLength = str(len(speechesID))
    countClinton = 1
    # Scanning all the speeches
    print "Starts The Scan"
    for id in speechesID:
        try:
            newURL = url + id
            print 'URL Number ' + str(countClinton) + ' of ' + speechesLength + '. URL: ' + newURL
            page = urllib2.urlopen(newURL)
            page_content = page.read()
            # Cleaning Data
            speech = str(page_content).split('displaytext')[2].split('noshade')[0].split('</span')[0].replace('"', '').replace('<p>', '').replace('</p>', '').replace('<i>', '').replace('</i>', '').replace('>', '').replace('The President. ','').replace('Q.','#').replace('Q:','#').replace('[Applause]','').replace('[applause]','').replace('[Laughter]','').replace('[laughter]','').replace('. ', '.\n')
            text = speech.split('\n')
            file_name = "Speech Number " + str(countClinton) + ".txt"
            open(clintonPath + '\\' + file_name, "w")
            # Writing the Speech to txt file
            for line in text:
                if (not '#' in line) or (not '[' in line) or (not '<' in line):
                    with open(clintonPath + '\\' + file_name, "a") as fid:
                        fid.write(line + "\n")
            countClinton += 1
            # Don't overload the server
            time.sleep(2)
        except:
            continue

if __name__ == "__main__":
    SpeechesFolder()