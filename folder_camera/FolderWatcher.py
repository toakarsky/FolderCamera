from os import listdir, path
import io
import sys

from PIL import Image

from .settings import FRAMERATE
from .settings import FOLDER_PATH
from .settings import SCALE_TO_SIZE
from .settings import DEBUG_MODE


class FolderWatcher:
    def __init__(self):
        self.loadedImagesData = []
        self.loadedImagesFilenames = []
        self.currentImageToRender = 0
    
    def getImagesFilenames(self):
        try:
            return listdir(FOLDER_PATH)
        except:
            print(f'[ERROR] READING IMAGES IN {FOLDER_PATH} FAILED')
            return []
    
    def loadImage(self, filename):
        image = Image.open(path.join(FOLDER_PATH, filename), mode='r')
        if SCALE_TO_SIZE != None:
            image = image.resize(SCALE_TO_SIZE)
        image = image.convert('RGB')
        
        imageBytes = io.BytesIO()
        image.save(imageBytes, format='JPEG')
        return imageBytes.getvalue()
        
    def refreshImagesList(self):
        currentImagesFilenames = self.getImagesFilenames()
        
        if currentImagesFilenames == self.loadedImagesFilenames:
            if DEBUG_MODE:
                print('[DEBUG] NO CHANGES DETECTED')
            return
        
        removedImagesFilenames = []
        for imageFilename in self.loadedImagesFilenames:
            if not imageFilename in currentImagesFilenames:
                if DEBUG_MODE:
                    print('[DEBUG]', imageFilename, 'WAS REMOVED')
                removedImagesFilenames.append(imageFilename)
        
        addedImagesFilenames = []
        for imageFilename in currentImagesFilenames:
            if not imageFilename in self.loadedImagesFilenames:
                if DEBUG_MODE:
                    print('[DEBUG]', imageFilename, 'WAS ADDED')
                addedImagesFilenames.append(imageFilename)
        
        for idx in range(len(self.loadedImagesFilenames) - 1, -1, -1):
            if self.loadedImagesFilenames[idx] in removedImagesFilenames:
                self.loadedImagesData.pop(idx)
                self.loadedImagesFilenames.pop(idx)
        
        for imageFilename in addedImagesFilenames:
            self.loadedImagesFilenames.append(imageFilename)
            try:
            # if True:
                self.loadedImagesData.append(self.loadImage(imageFilename))
            except:
                if DEBUG_MODE:
                    print(f'[DEBUG] {imageFilename} IS BROKEN, SKIPPING')
                self.loadedImagesFilenames.pop()
            else:
                if DEBUG_MODE:
                    print(f'[DEBUG] {imageFilename} IS OK')
        
        if len(self.loadedImagesFilenames) != 0:
            self.currentImageToRender = self.currentImageToRender % len(self.loadedImagesFilenames)
                
    def getFrame(self):
        if len(self.loadedImagesFilenames) == 0:
            if DEBUG_MODE:
                print('[DEBUG] NO LOADED IMAGES')               
                print('[DEBUG] CURRENT FRAME IS NONE')
            return None
        
        currentFrame = self.currentImageToRender
        self.currentImageToRender += 1
        self.currentImageToRender %= len(self.loadedImagesFilenames)
        
        if DEBUG_MODE:
            print(f'[DEBUG] CURRENT FRAME IS {self.loadedImagesFilenames[currentFrame]}')
        return self.loadedImagesData[currentFrame]
