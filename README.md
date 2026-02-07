https://github.com/user-attachments/assets/0fc27f43-3472-4f73-902b-ac11e8c6fe60

# Problem Statement for inspiration
Consider a long steel annular pipe of 5 cm outer radius and 2 cm inner radius with k=45 W/m-°C and α=1.16 x 10-5 m2/s. This pipe was initially at 200 °C and the inner surface is insulated. Now, the upper half of the rod (mentioned in part a) is exposed air at 20° C with h= 50 W/m2-°C, and, the lower half is placed into a cooling water flow at 5° C with h= 250 W/m2-°C. Find out the time in which the maximum temperature inside the rod will be less than 100 °C.

Consider this as a polar coordinate heat transfer problem and show the formulation of the problem including discretized equations at internal points and boundaries. Mention about your solution scheme. Report solutions for two different grid sizes. Show the temperature contour at the desired time.

# Methodology
The mathematical details and discretization used for this heat flow problem is mentioned in `./report.pdf` along with the generated results for multiple setups (at that time I screen recorded for transparency).

# `./code.py`
Used to generate the matplotlib animation for the simulation where each frame is updated by the discritized updation equation (relation giving temperature at each point at next time step only by using temperature nearby at current time step). The animation is set to stop only when every point in the tube comes below 100 °C. If the `slowdown` parameter is set to 1, it would be ideally as 1:1 flow temporally.

# `./speedup.py`
The generated video is written to not have much control over the video length. To get a sped up video compressed in some set total time length, this program can be used. This code don't have any realtion with CFD techniques. Its purely video speeding program.
**Overview of the method** : According to the length, new frame rate is calculated, if its larger than 100 Hz, frame skipping is done to ensure this capped frame rate is maintained while the resulting video length is exactly that desired by the user.

# Usage

	chmod +x ./run.sh
	./run.sh

Find the original video in `./org` directory and sped up video in `./res`
