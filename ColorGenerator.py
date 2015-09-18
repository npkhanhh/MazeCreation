'''
Created on Sep 18, 2015

@author: ldhuy
'''

class ColorGenerator(object):
    '''
    Generate RGB code randomly in a way that results colors are as distinct as possible
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.h = 0
        self.golden_ratio_conjugate = 0.618033988749895
        
    def hsv_to_rgb(self, h, s, v):
        h_i = float(h)/60
        c = v*s
        x = c*(1-abs(h_i%2 - 1))
        if h_i == 0:
            r, g, b = [0, 0, 0] 
        elif h_i < 1:
            r, g, b = [c, x, 0] 
        elif h_i < 2:
            r, g, b = [x, c, 0] 
        elif h_i < 3:
            r, g, b = [0, c, x] 
        elif h_i < 4:
            r, g, b = [0, x, c] 
        elif h_i < 5:
            r, g, b = [x, 0, c]
        elif h_i < 6:
            r, g, b = [c, 0, x]
            
        m = v - c
        r += m
        g += m
        b += m
        
        r = r * 255
        g = g * 255
        b = b * 255
        return [int(r), int(g), int(b)]
    
    def rgbCodeToHexString(self, r, g, b):
        rh = hex(r)
        gh = hex(g)
        bh = hex(b)
        
        rh = rh[2:]
        gh = gh[2:]
        bh = bh[2:]
        
        return rh + gh + bh
    
    def randomColorCode(self):
        self.h += self.golden_ratio_conjugate
        self.h = self.h % 1
        h = self.h * 360
        rgb = self.hsv_to_rgb(h, 0.5, 0.95)
        code = self.rgbCodeToHexString(rgb[0], rgb[1], rgb[2])
        return code