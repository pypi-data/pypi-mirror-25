from pylab import * 

def convolve(self,axisname,filterwidth,convfunc = (lambda x,y: exp(-(x**2)/(2.0*(y**2))))):
    r'''perform a normalized convolution'''
    #{{{ make a version of x that is oriented along the correct dimension
    x = self.getaxis(axisname).copy()
    x_centerpoint = (x[-1]+x[0])/2
    x -= x_centerpoint # so that zero is in the center
    x = ifftshift(x) # so that it's convolved about time 0
    thisaxis = self.axn(axisname)
    #}}}
    myfilter = convfunc(x,filterwidth)
    myfilter /= myfilter.sum()
    filtershape = ones_like(self.data.shape)
    filtershape[thisaxis] = len(myfilter)
    myfilter = myfilter.reshape(filtershape)
    #self.data = ifftshift(ifft(fftshift(fft(self.data,axis = thisaxis),axes = thisaxis)*fftshift(fft(myfilter,axis = thisaxis),axes=thisaxis),axis = thisaxis),axes = thisaxis) # for some reason fftconvolve doesn't work!
    self.data = ifft(fft(self.data,axis = thisaxis)*fft(myfilter,axis = thisaxis),axis = thisaxis)
    #self.data = fftconvolve(self.data,myfilter,mode='same') # I need this, so the noise doesn't break up my blocks
    return self
