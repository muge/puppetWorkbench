# Puppet Workbench v0.7c
_Originally posted to XenTaX.com on 2018/10/20_  
by mug

Converts images that can be used to mod in custom portraits for **Labyrinth of Refrain: Coven of Dusk (PC)**.  
**Labyrinth of Galleria: The Moon Society** uses different filenames (will need to adapt) but I've been told it otherwise uses identical image formats. YMMV.

See also companion script, [puppetFacebench](https://github.com/muge/puppetFacebench), which can and should inhabit the same folder as this script for ease of use.

## I. Pre-amble, License & Disclaimer   
Kinda jank script that automates what is essentially repacking .dds.phyre files.    
The concept is taking DDS image data and attaching it to the end of an "empty" .dds.phyre file of the same type.  

This work is now licensed under GNU General Public License v3.0, please refer to the included LICENSE file.  
*<sub>This was FORMERLY licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License, which may be found in various archived (pre-2025) versions of this script around the internet.</sub>*

**DISCLAIMER**:  
By using this script you agree that I'm not responsible if you muck up your files (game-related or otherwise) or computer beyond repair.  
Script was only (briefly) tested on Windows 7 64-bit, using Python 3.7.0 32/64-bit.

## II. Things you'll need
1. Python 3.7.0 (https://www.python.org/downloads/release/python-370/) 
	* PROTIP: check add Python 3.7 to PATH when installing
2. Install Pillow (cmd to your python.exe directory "python -m pip install Pillow")
	* If this doesn't work, you're figuring it out yourself, may have to do with Windows PATH environmental variable?
3. Photoshop with NVIDIA's DDS Plugin installed (https://developer.nvidia.com/nvidia-texture-tools-adobe-photoshop)
4. (Optional) Noesis with .PHYRE plugin ([https://zenhax.com/viewtopic.php@t=7573.html](https://zenhax.com/viewtopic.php@t=7573.html))
	* Very helpful for testing/viewing/extracting files
5. Basic Photoshop skills
6. Patience


## III. Prepping Files
**NOTE: BACK UP THE FILES YOU'RE EDITING BEFORE REPLACING, OTHERWISE THE ONLY WAY TO REVERT IS TO REINSTALL THE GAME!**  
*Also important to note: Back up your save before reinstalling!*

In order to create a complete custom portrait mod, you must make each of the following versions of the images the game uses.  
*Image dimensions MUST match!*

Full-sized portraits
| Full_Length_XXX.dds.phyre | |
|:-|:-|
|4K | 2048 x 2048 |
| HD | 1024 x 1024 |

Small portraits
| wf_XXX.dds.phyre | |
|:-|:-|
|4K | 1024 x 512 |
| HD | 512 x 256 |

Small icons
|CharaFace_Icon.dds.phyre| |
|:-|:-|
|4K| 2048 x 1536|
|HD| 1024 x 768|

Chibis
|minichara_XX_XX_XXX.dds.phyre| |
|:-|:-|
|4K | 1024 x 1024|
|HD | 512 x 512|
 
*There is also the CharaFace_Icon sheet, which is handled by [puppetFacebench](https://github.com/muge/puppetFacebench), a companion script for puppetWorkbench.*

### Saving your Images
After you're finished making edits to your .PNG image, you need to do a few more things in Photoshop.
1. Image > Image Rotation > Flip Vertical
2. File > Save as, choose *.DDS on the extension dropdown
3. When the window pops up, choose the right compression (I actually don't think it matters but in case it does):
   - DXT5: Full-sized or Small Portraits
   - DXT3: Chibi and CharaFace_Icon
4. Everything else should be unchecked, select "Transparency" under Alpha Channel.
* Sometimes images will muck up for no discernable reason. When this happens, try saving with the Pre-Multiply option on the DDS export window ticked.

## IV. Usage
This is a CLI-style script that takes typed user inputs, so observe the below. 
The syntax is as follows:  
### inputFile modName [-class -palette -chibi]

1. Save or move the .DDS you just made into the same folder as puppetWorkbench.py
2. Run puppetWorkbench.py, or drag the .DDS file onto it.
3. Specify the inputs, following the syntax.

There are a few examples later on in this README.

--------
### **Input file**  
- **CANNOT** have spaces in its name.
- Must be in the same folder as the script
- Can be dragged onto the script file (do not need to specify if you do)  
- Must be the first parameter.

--------
### **modName**  
- Determines destination and prefix of files, mainly for organizational purposes.
    - ex. `mods\modName\modName.[filename].dds.phyre`
- Must be specified after the input filename. 
- Illegal characters will be stripped. 

--------
### **[-options]**
- Can be input in any order.  
- **CharaFace_Icon will not take any parameters.**

#### Chibi or minichara
**-chibi**  
- Must be specified if it's a "minichara" (chibi) file.

#### Classes (Facets):
- Easy way to remember the facets are that **-m** and **-f** are used to denote gender, followed by the initials of the class.  
    - Note that Gothic Coppelia and Demon Reaper only have one gender.  

| Facet | Male | Female |
|:----------------|:-----|:-------|
| Aster Knight | -mak | -fak |
| Peer Fortress | -mpf | -fpf  |
| Shinobushi | -msb | -fsb |
| Mad Raptor | -mmr | -fmr  |
| Theatrical Star | -mts | -fts  |
| Marginal Maze | -mmm | -fmm  |
| Gothic Coppelia | | -gc  |
| Demon Reaper | | -dr  |
         
#### Palette: 
**-1p**, **-2p**, **-3p**, or **-4p**  
- Will generate files for all 4 palettes if left blank.

--------


### EXAMPLES: 
- Full-Sized Female Aster Knight Portrait for Palette 1:  
```input.dds babbysFirstMod -fak -1p```

- CharaFace_icon: (do not include other params)  
```input.dds babbysFirstMod```
	
- Demon Reaper Chibi, all palettes: (does not take gender)  
```input.dds babbysFirstMod -dr -chibi```
	
- Female Marginal Maze Battle Portrait, all palettes:  
```input.dds babbysFirstMod -fmm```

NOTE: Remember, image-types are detected automatically by dimension hence they are not specified in the parameters.

4. Output files will be in the `\mods\` folder under the modName you specified.  
	Said files can then be zipped up and distributed as such.


Hopefully you understand a bit better how to use this now.

## V. "Installation" of files
**IMPORTANT: IF YOU HAVEN'T BACKED UP YOUR FILES, NOW'S A GOOD TIME!**

Image mods you've created are essentially replacing files in your game's folder.  
1. Remove the modName's prefixes by renaming the files (or you can do this after you pasted, whatever)  
2. Copy and paste the .dds.phyre files from the folder generated to the following locations:  

| Full_Length_XXX.dds.phyre <br> CharaFace_Icon.dds.phyre <br> and <br> wf_XXX.dds.phyre  |
|:-|
|```[Game Install Directory]\Media\D3D11\Majo\texture\model\ui\```|

|minichara_XX_XX_XXX.dds.phyre  |
|:-|
|```[Game Install Directory]\Media\D3D11\Majo\texture\model\effect\```|

puppetWorkbench will generate a HELP.txt inside each folder containing the path information above.

Hope you backed up your files before overwriting.  
You're done!

--------
### "Uninstallation"
Paste and overwrite from your backed up files.  
Otherwise, reinstall the game (Important: back up your save before reinstalling!)


## VI. Image-editing (bonus tips)
You can use the files inside templates.zip, which contains some photoshop .PSDs and sample images you may find helpful. These ones are already vertically flipped.  
For CharaFace_Icon, please refer to [puppetFacebench](https://github.com/muge/puppetFacebench) and CharaFace_Icon* template files. These ones are NOT vertically flipped.  

--------
### Changelog
```
- v0.00 - v0.1  
	Initial proof of concept ver.  
	Shoddy README.txt  
- v0.2  
	Updated for Python 3.7 (from 2.7)  
	Removed image-type parameters in favor of auto-detecting image  
- v0.3  
	Script now uses stripped-down template files rather than needing to read from files in Game Directory (which was a bad idea in the first place)  
	Script no longer closes once finished or on caught(fml) errors  
	Image validation/detection now makes more sense  
- v0.4  
	Added support for CharaFace_Icon conversion  
	Added "all palette" functionality  
- v0.5  
	Bugfixing for Gothic Coppelia and Demon Reaper filename generation  
	Bugfixing for CharaFace_Icon offsets  
	Added "help" command  
- v0.6  
	Added drag-drop support  
	Added more verbose file/option error feedback  
	Added HELP.txt to output to folders  
	Fixed issue with leading zeroes  
	Fixed files being generated with wrong size (and not read by the game)  
	Rewrote README.txt  
- v0.7  
	Combined class and gender parameters.  
	Fixed first minichara sheet being numbered incorrectly (from 0.7a)  
	Removed /templates/ folder so they can be downloaded separately  
	Minor updates to the README with the release of puppetFacebench  
	Additional files added to templates.zip
        Rewrite and reformat README in markdown for GitHub
```
