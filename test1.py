import cv2
import numpy as np
cap = cv2.VideoCapture("videos/pivideo3.mp4")

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.1,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
feat_reg_mask = np.zeros_like(old_gray, dtype=np.uint8)
feat_reg_mask[int(0.49 * old_gray.shape[0]):int(0.8 * old_gray.shape[0]), int(0.1 * old_gray.shape[1]):int(0.9 * old_gray.shape[1])] = 255
p0 = cv2.goodFeaturesToTrack(old_gray, mask = feat_reg_mask, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
timer = 0
last_dirs = None

while(1):
    timer += 1
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    
    if (p1 is None) or (timer % 5 == 0):
        cv2.imshow('frame',frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        old_gray = frame_gray.copy()
        p0 = cv2.goodFeaturesToTrack(old_gray, mask = feat_reg_mask, **feature_params)
        mask = np.zeros_like(old_frame)
        
    else:

        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]

        # draw the tracks
        avg_dir = np.zeros(2)
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            avg_dir += (new - old)
            mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
            frame = cv2.circle(frame,(a,b), 3, color[i].tolist(),-1)
        
        img = cv2.add(frame,mask)
        
        if last_dirs is None:
            last_dirs = np.zeros((7, 2))
            for i in range(7):
                last_dirs[i] = avg_dir
        else:
            last_dirs = np.roll(last_dirs, -1)
            last_dirs[-1] = avg_dir
        avg_dir = np.mean(last_dirs, axis=0)
        avg_dir[1] = 0
        center = (img.shape[1]//2, img.shape[0]//2)
        dir_mask = cv2.line(img, center, tuple((avg_dir / 3).astype(int) + center), [255, 255, 255], 4)
        
        
        diffs = np.zeros(good_new.shape[0])
        for i,(new, old) in enumerate(zip(good_new, good_old)):
            expected_dir = avg_dir + (old - center) * 0.05 # TODO: use speed
            diffs[i] = np.linalg.norm((new-old) - expected_dir)
        
        diffs = diffs * good_new.shape[0] / np.sum(diffs)
        diff_mask = np.zeros_like(img)
        for i,(new, old) in enumerate(zip(good_new, good_old)):
            diff_mask = cv2.circle(frame, tuple(new), int(diffs[i] * 10), [255, 0, 0], -1)
        img = cv2.add(img, diff_mask)

        cv2.imshow('frame',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == ord('p'):
            k1 = cv2.waitKey()
            if k1 == 27:
                break

        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()
cap.release()
