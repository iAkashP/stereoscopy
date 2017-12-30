# Stereoscopy
fusing two 2D images, giving 3 dimensional visual impression, giving depth to image and finding the depth.

## prerequisites:
1. OpenCV module
2. knowledge on camera focal length, FOV
3. Two same cameras with similar FOV,focal length

## change on code:
some changes to be considered in the final equation:

fin_dist=B*foc_len/(2*np.tan(fi/2)*D)

B=distance between two cameras;
foc_len=focal length of cameras;
fi=FOV of camera;
D=*already calculated

### for more information,refer:
http://dsc.ijs.si/files/papers/s101%20mrovlje.pdf
