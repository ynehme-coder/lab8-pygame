# MY NOTES #
# For the flee function
The smaller squares should "flee" when they get approached by the larger squares meaning they should change their course to a opposite direction. The distance should be from the center of the square not the edges.

# For the life/rebirth feature
For the life/rebirth feature I need to make a randomly generated timer for each square and add a destroy square function inside the update_squares fn. Rebirth should probably be instantanuous when a square gets destroyed.

# The chase feature
I'm thinking I should split the chase function into 2:  a nearness function that finds the nearest small square, and a chase function that moves the big square in that direction. I can repurpose sections of the flee functions to make both functions.