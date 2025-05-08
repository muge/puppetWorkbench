 # Python 3.7 and Pillow required
 # Puppet Workbench for Labyrinth of Refrain: Coven of Dusk (PC)
 # v0.7c by mug
import os, sys, mmap, shutil, pathlib, msvcrt, time
from PIL import Image

script_dir = os.path.dirname(__file__) #os.path.join(script_dir, rel_path)
valClas = ['-mak', '-fak', '-msb', '-fsb', '-mts', '-fts', '-mmm', '-fmm', '-mpf', '-fpf', '-mmr', '-fmr', '-gc', '-dr']
valPalt = ['-1p', '-2p', '-3p', '-4p']
inWidth = ['2048', '1024', '512'] 
inHeight = ['2048', '1536', '1024', '768', '512', '256']
vTypeList = ['Full_Length_0XX.dds.phyre', 'Full_Length_0XX_4k.dds.phyre', 'minichara_0X_0X_0XX.dds.phyre', 'minichara_0X_0X_0XX_4k.dds.phyre', 'CharaFace_icon.dds.phyre', 'CharaFace_icon_4k.dds.phyre', 'wf_0XX.dds.phyre', 'wf_0XX_4k.dds.phyre']
clear = lambda: os.system('cls')
run = True
dragFile = False

def motd():
    print("Puppet Workbench v0.7c by mug")
    print("'Read the goddamn README edition'")
    print("-------------------------------------------------")
    print("Syntax: input.dds modName [-options]")
    print("Refer to README or enter \"help\".")
    print("-------------------------------------------------")
    return

def help():
    print("Read the README!")
    print("-------------------------------------------------")
    print("Input DDS file can be dragged onto puppetWorkbench.py.")
    print("      Must be in the same folder as puppetWorkbench.py.")
    print("      CANNOT have spaces in the filename.")
    print("modName determines destination and prefix of files.")
    print("      MUST be specified after input file.")
    print("-------------------------------------------------")
    print("-options can be input in any order.")
    print("-options are not needed for CharaFace iconsheets,")
    print("         but are required for all other files.")
    print("-------------------------------------------------")
    print("Must specify -chibi if it's a minichara file.")
    print("-------------------------------------------------")
    print("Classes: -mXX/-fXX denote gender.")
    print("       -mak/-fak: Aster Knight     -mpf/-fpf: Peer Fortress")
    print("       -msb/-fsb: Shinobushi       -mmr/-fmr: Mad Raptor")
    print("       -mts/-fts: Theatrical Star  -gc: Gothic Coppelia")
    print("       -mmm/-fmm: Marginal Maze    -dr: Demon Reaper")
    print("-------------------------------------------------")
    print("Palette: -1p, -2p, -3p, or -4p")
    print("Leaving blank will generate files for all 4 palettes.")
    print("-------------------------------------------------")
    print("Example:\nminichara.dds babbysFirstMod -fmm -2p -chibi")
    return

def valArg(inputVal, drg, load): #validate input and feedback
    while True:
        try:
            inputLine = input(inputVal)
            inputTemp = inputLine.split()
            if drg is True:
                loadedFile = load
                inputTemp.insert(0, loadedFile)
                
            vinFile = inputTemp[0]
            voutFix = inputTemp[1]
            # strip illegal characters
            remove_punctuation_map = dict((ord(char), None) for char in '\/*?:"<>|')
            voutFix.translate(remove_punctuation_map)
            var = inputTemp[2:]
            vinFile = Image.open(vinFile)
            outputLine = " ".join(inputTemp) #output new vars
        except IndexError:
            if inputTemp[0] == "help":
                help()
            else:
                print("Missing parameters or invalid input.")
            continue
        except IOError:
            print("Invalid DDS file.")
            continue
        except:
            print("uhhh????")
            continue
        if drg is True and inputTemp[1] == "help":
            help()
        if vinFile.format is not "DDS":
            print("Input file must be DDS")
            continue
        if str(vinFile.width) not in inWidth or str(vinFile.height) not in inHeight:
            print("Invalid image dimensions. Refer to README.")
            continue 
        if bool(set(var).intersection(valClas)) is False:
            if vinFile.width == 2048 or vinFile.width == 1024: #if charaface
                if vinFile.height == 1536 or vinFile.height == 768:
                    set(var).intersection(valClas)    
            else:
                print("ERROR: Missing facet specification. Refer to README.")
                continue
        else:
            if len(set(var).intersection(valClas)) > 1:
                print("ERROR: More than one facet specified.")
                continue
        if bool(set(var).intersection(valPalt)) is False:
            print("Missing or invalid palette selection, defaulting to all.")
        else:
            if len(set(var).intersection(valPalt)) > 1:
                print("ERROR: More than one Palette specified.")
                continue
        #print("done validation")
        break
    return outputLine

def detType(inputFile, chb): # determine image type via dimensions:
    if inputFile.width == inputFile.height: #not WF or icon
        if inputFile.width == 2048:
            print(">>> 4K Full Portrait selected.")
            vImgType = "FL4K"
        elif chb is False:
            print(">>> HD Full Portrait selected.")
            vImgType = "FLHD"
        elif chb is True:
            if inputFile.width == 1024:
                print(">>> 4K Chibi selected.")
                vImgType = "MC4K"
            else:
                print(">>> HD Chibi selected.")
                vImgType = "MCHD"
    elif inputFile.height == 1536 or inputFile.height == 768: #not wf, must be icon
        if inputFile.width == 2048:
           print(">>> 4K Face Icon sheet selected.")
           vImgType = "CF4K"
        else:
           print(">>> HD Face Icon sheet selected.")
           vImgType = "CFHD"
    elif inputFile.width == 1024 and inputFile.height == 512:
        print(">>> 4K Face Portrait selected.")
        vImgType = "WF4K"
    elif inputFile.width < 1024 and inputFile.height == 256:
        print(">>> HD Face Portrait selected.")
        vImgType = "WFHD"
    return vImgType

def detNum(imgtype, varList, mode): #determines filenames and number(s) for type
    chkPal = bool(set(varList).intersection(valPalt))
    chkCls = bool(set(varList).intersection(valClas))
    
    if "CF" in imgtype: # if it's CharaFace ignore them and just set them to 0
        pal = 0
        cls = 0
        clsInd = 0
        gen = 0
        genNum = 0
    else:
        cls = str(set(varList).intersection(valClas))[2:-2]
        #print(str(varList))
        clsInd = int(valClas.index(cls)) # get index of cls
        #print(clsInd)
        if chkPal is True: # palette was specified
            pal = str(set(varList).intersection(valPalt))[2:-2] # remove curlies and quotes
            palNum = int(pal[1:-1])-1 # remove -p
        else:
            pal = "-1p"
            palNum = 0

    app4K = "" if "4K" not in imgtype else "_4k"
    if "CF" not in imgtype:
        clsNum = clsInd*4+1 #print("pal: "+str(pal)+" cls: "+str(clsNum)+" / "+str(clsInd)+" gen: "+str(gen))
        gen = clsInd%2
        #if cls
    if mode == "final":
        if "MC" in imgtype:
            if clsInd < 13: #hardcode for DR
                mcInd = int(clsInd/2)
            else:
                mcInd = 7
            if clsInd == 12: #hardcode for GC
                gen = 2
            output = ["minichara_0"+str(mcInd)+"_0"+str(gen)+"_00"+str(palNum+1)+app4K+".dds.phyre"]
            if chkPal is False:
                for i in range(1,4): 
                    print(mcInd)
                    output.append("minichara_0"+str(mcInd)+"_0"+str(gen)+"_00"+str(palNum+1+i)+app4K+".dds.phyre")
                    
        elif "FL" in imgtype or "WF" in imgtype:
            num = clsNum+palNum
            if "FL" in imgtype:
                output=["Full_Length_0"+str("{:02}".format(num))+app4K+".dds.phyre"]
                if chkPal is False:
                    for i in range(1,4):
                        output.append("Full_Length_0"+str("{:02}".format(num+i))+app4K+".dds.phyre")                        
            else:
                output=["wf_0"+str("{:02}".format(num))+app4K+".dds.phyre"]
                if chkPal is False:
                    for i in range(1,4):
                        output.append("wf_0"+str("{:02}".format(num+i))+app4K+".dds.phyre")
        elif "CF" in imgtype:
            output = ["CharaFace_icon"+app4K+".dds.phyre"]
    else: #mode is template
        if "FL" in imgtype:
            output=["Full_Length_0XX"+app4K+".dds.phyre"]
        elif "MC" in imgtype:
            output=["minichara_0X_0X_0XX"+app4K+".dds.phyre"]
        elif "WF" in imgtype:
            output=["wf_0XX"+app4K+".dds.phyre"]
        else:
            output=["CharaFace_icon"+app4K+".dds.phyre"]
    return output
  
def doMk(inputVal):
    print(inputVal)
    inputTemp = inputVal.split()
    vinFile = inputTemp[0]
    vinFile = Image.open(vinFile)
    voutFile = inputTemp[1]
    # strip illegal characters
    remove_punctuation_map = dict((ord(char), None) for char in '\/*?:"<>|')
    voutFile.translate(remove_punctuation_map)
    var = inputTemp[2:]
    print(var)
    if len(var) > 1: #not CharaFace
        chkPl = bool(set(var).intersection(valPalt))
        chkMc = bool("-chibi" in var)
        palLoop = 1 if chkPl is True else 4
    else:
        #var = [0]
        chkPl = False
        chkMc = False

    pathlib.Path('mods/'+inputTemp[1]).mkdir(parents=True, exist_ok=True)
    print(chkMc)
    vImgType=detType(vinFile, chkMc)
    templateName = detNum(vImgType, var, "template")[0]
    outName = detNum(vImgType, var, "final")
    finName = [0,0,0,0]
    finPath = [0,0,0,0] # lol pro as fuck don't look
    
    for i in range(1):
        #print(str(i)+" "+str(finName))
        finName[i] = voutFile+"."+outName[i]
        finPath[i] = script_dir+"\\mods\\"+voutFile+"\\"+finName[i]
        #print (detNum(vImgType, var, "template")[i]+", "+detNum(vImgType, var, "final")[i])
        # copy template to output folder to prep
        shutil.copy(script_dir+"\\src_temp\\"+templateName, finPath[i])
    
    with open (inputTemp[0],"r+b") as inDDS:
        inMMAP = mmap.mmap(inDDS.fileno(), 0)
        # get total bytes in file
        inMMAP.seek(0,2)
        ddsEOF = inMMAP.tell()
        if "CF" not in vImgType:
            offSIN = 136 #136 is 88, aka where image data starts
        else:
            offSIN = 140 #140 is 8C
        inMMAP.seek(offSIN) 
        bRemain = inMMAP.tell() - ddsEOF
        DDSHEX = inMMAP.read(bRemain)

        with open (finPath[0], "r+b") as outPHYRE: #open the output to write to
            outMMAP = mmap.mmap(outPHYRE.fileno(), 0)
            outMMAP.seek(0,2) 
            newSize = inMMAP.size()+outMMAP.size()-offSIN
            outMMAP.resize(newSize)
            outMMAP.write(DDSHEX)
            outMMAP.seek(0) #go back to beginning
            if "CF" not in vImgType: #rewrite path in file
                if "MC" not in vImgType: 
                    outMMAP.seek(2445) #98D
                else:
                    outMMAP.seek(2449) #991
                b = outName[0][:-6].encode('utf-8')
                outMMAP.write(b)
            outMMAP.flush()
            outMMAP.close()
        inMMAP.flush()
        inMMAP.close()

        if chkPl is False and "CF" not in vImgType: # do 3 more if palette not specified
            for i in range(1,4):
                finName[i] = voutFile+"."+outName[i] #print(finName[i])
                finPath[i] = script_dir+"\\mods\\"+voutFile+"\\"+finName[i]
                shutil.copy(finPath[i-1], finPath[i])
                with open (finPath[i],"r+b") as outPHYRE:
                    reMMAP = mmap.mmap(outPHYRE.fileno(), 0)
                    reMMAP.seek(0)#go back to beginning
                if "CF" not in vImgType: #rewrite path in file
                    if "MC" not in vImgType: 
                        reMMAP.seek(2445) #98D
                    else:
                        reMMAP.seek(2449) #991
                    b = outName[i][:-6].encode('utf-8')
                    #print(b)
                    reMMAP.write(b)
                reMMAP.flush()
            reMMAP.close()
    with open(script_dir+"\\mods\\"+voutFile+"\\HELP.txt", "w") as hTXT:
        hTXT.write("BACK UP YOUR FILES!\n\nInstall Locations:\n\nFull_Length_XXX.dds.phyre,\nCharaFace_Icon.dds.phyre,\nwf_XXX.dds.phyre:\n       [Game Install Directory]\\Media\\D3D11\\Majo\\texture\\model\\ui\\ \n\nminichara_XX_XX_XXX.dds.phyre:\n       [Game Install Directory]\\Media\\D3D11\\Majo\\texture\\model\\effect\\")
    print("Complete! Check the \\mods\\"+voutFile+"\\ folder.")
    return

def main():
    motd()
    if len(sys.argv) > 1:
        dragFile = True
        loadFile = str(os.path.basename(sys.argv[1]))
        loadString = "Loaded: "+loadFile+" "
        inputs = valArg(loadString, dragFile, loadFile)
    else:
        dragFile = False
        loadFile = ""
        inputs = valArg("Input: ", dragFile, loadFile)
    doMk(inputs)
    return

def wait():
    try:
        if dragFile is True:
            drg = " on loaded file, or close to exit."
        else:
            drg = "."
        input(">>> Hit ENTER to continue"+drg)        
    except ValueError:
        print("Something fucked up, just close and re-run I guess lmao")
        pass

while run == True:
    main()
    run = False
    wait()
    clear()
    run = True
