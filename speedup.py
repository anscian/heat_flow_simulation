import cv2
import sys


def speedup(src, length=10, max_fps=100, output='res/out.mp4'):
	cap = cv2.VideoCapture(src)
	if not cap.isOpened():
		return

	fps = int(cap.get(cv2.CAP_PROP_FPS))
	frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

	print(fps, frames, width, height)

	new_fps = frames//length
	skip_frames = new_fps//max_fps

	print(new_fps, skip_frames, max_fps)

	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	out = cv2.VideoWriter(output, fourcc, min(max_fps, new_fps), (width, height))

	if new_fps < max_fps:
		while True:
			ret, frame = cap.read()
			if not ret:
				break
			out.write(frame)
	else:
		count = 0
		while True:
			ret, frame = cap.read()
			if not ret:
				break
			if count == 0:
				out.write(frame)
			count = (count + 1) % skip_frames

	cap.release()
	out.release()


if __name__ == '__main__':
	#speedup('org/r10th15dt0.1.mp4', output='res/r10th15dt0.1.mp4')
	#speedup('org/r30th30dt0.01.mp4', output='res/r30th30dt0.01.mp4')
	#speedup('org/r100th100dt0.01.mp4', output='res/r100th100dt0.01.mp4')
	speedup(sys.argv[1], output=sys.argv[2], length=int(sys.argv[3])) # speed up the generated video in org to desired length in seconds
