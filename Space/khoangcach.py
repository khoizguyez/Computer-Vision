import cv2
import numpy as np

# Known width of the object (cm)
# KNOWN_WIDTH = 20.0  # Width of the star in cm

KNOWN_WIDTH = 50.0  # Width of the star in cm
focal_length = 0  # Initialize focal length

# Create a black image
img = np.zeros((512, 512, 3), np.uint8)

# Draw the star
star = np.array([[200,100],[200,191],[114,219],[200,247],[200,338],[254,264],[340,292],[287,219],[340,146],[254,174]], np.int32)
star = star.reshape((-1,1,2))
# cv2.polylines(img, [star], True, (0, 0, 255), 5)
cv2.polylines(img, [star], True, (15, 51, 100), 5)

# Read the video
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)

    # Blur the image to reduce noise (optional)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply edge detection
    # edges = cv2.Canny(blurred, 50, 150)
    
    # edges = cv2.Canny(blurred, 300, 550)
    edges = cv2.Canny(blurred, 100, 150)

    # Find contours
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # Calculate the bounding box
        (x, y, w, h) = cv2.boundingRect(cnt)

        # Calculate aspect ratio
        aspect_ratio = float(w) / h

        # Check if aspect ratio is close to 1 and minimum area threshold
        if abs(aspect_ratio - 1) < 0.2 and cv2.contourArea(cnt) > 100:
            # Calculate focal length (assuming object fills most of the frame initially)
            if focal_length == 0:
                focal_length = (w * KNOWN_WIDTH) / w

            # Calculate distance based on known width and focal length
            distance = (KNOWN_WIDTH * focal_length) / w

            # Draw rectangle around the detected star in red color
            # cv2.polylines(frame, [star], True, (0, 0, 255), 5)

            # Display distance
            cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the image
    cv2.imshow(winname="Frame", mat=frame)

    # Exit when escape is pressed
    if cv2.waitKey(delay=1) == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
