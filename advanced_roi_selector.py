import os
import cv2
import imutils

current_dir = os.getcwd()
cam='0'

roi_coord=[]

def remove_file(path, file_name):
    # check if file exists or not
    if os.path.exists(str(path) + '/' + str(file_name)) is False:
        # file did not exists
        return True
    else:
        os.remove(str(path) + '/' + str(file_name))


def roi_creation():
    global roi_coord
    global ix,iy,vx,vy,mouse_flag

    if os.path.isfile("roi_line_config.txt"):
        try:
            file1 = open("roi_line_config.txt", "r+")

            t = file1.read()
            # print(t.split("\n"))
            roi_coord = t.split("\n")
            line_type=roi_coord[-2]
            # print(roi_coord)
            i = 0
        except IndexError:
            file9 = open("error_logs.txt", "w")
            file9.write("list index out of range...i.e.roi selection is not done propperly values missing..delete roi_line_config.txt and run again...")
            print("failure")

            path = str(current_dir)
            file_name = "roi_line_config.txt"
            remove_file(path, file_name)
            exit(0)

        print("success")

    else:

        ix, iy = -1, -1
        vx, vy = 1, 1
        mouse_down = False
        mouse_flag = 0
        x = y = w = h = 0
        line_type=''
        if cam == str(0) or cam == str(1):
            cap = cv2.VideoCapture(int(cam))
        else:
            cap = cv2.VideoCapture(str(cam))

        rectangle_flag = 0



        print(" 'r' for rect roi selection , l for line ,'q' for exit selection mode")
        x = y = w = h = 0
        rectangle_flag = 0
        line_flag = 0
        file1 = open("roi_line_config.txt", "w")

        while (True):  # to select roi loop

            # Capture frame-by-frame
            ret, frame = cap.read()
            frame_new = frame
            frame = imutils.resize(frame, width=800)
            frame_new = imutils.resize(frame, width=800)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("r") or key == ord("R"):
                initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
                # print(initBB)
                ll = list(initBB)
                x = initBB[0]
                y = initBB[1]
                w = initBB[2]
                h = initBB[3]
                roi_coord.insert(0, initBB[0])
                roi_coord.insert(1, initBB[1])
                roi_coord.insert(2, initBB[2])
                roi_coord.insert(3, initBB[3])



                cv2.destroyAllWindows()



                while True:
                    if roi_coord[0] == '0' and roi_coord[1] == '0' and roi_coord[2] == '0':

                        print("Please Select ROI properly...")
                        initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
                        ll = list(initBB)
                        x = initBB[0]
                        y = initBB[1]
                        w = initBB[2]
                        h = initBB[3]
                        roi_coord.insert(0, initBB[0])
                        roi_coord.insert(1, initBB[1])
                        roi_coord.insert(2, initBB[2])
                        roi_coord.insert(3, initBB[3])


                    else:
                        break

                rectangle_flag = 1
                file1.write(str(initBB[0]) + "\n")
                file1.write(str(initBB[1]) + "\n")
                file1.write(str(initBB[2]) + "\n")
                file1.write(str(initBB[3]) + "\n")

            if key == ord("l"):
                # cv2.imshow('frame_new', frame)
                cv2.destroyAllWindows()

                line_type = input("enter lineType 'h' for Horizontal,'v' for vertical..\n")
                print(line_type)

                while True:
                    print_flag = 1
                    if (line_type != 'h' and line_type != 'v'):
                        if print_flag == 1:
                            print("invalid_cradentials,reenter line credentials press l.. ")
                            line_type = input("enter lineType 'h' for Horizontal,'v' for vertical..\n")

                            print_flag = 0
                    elif (line_type == 'h' or line_type == 'v'):
                        break

                print("\n")
                cv2.destroyAllWindows()

                # cv2.setMouseCallback('frame', line)

                roi_coord.insert(10, line_type)
                roi_coord.insert(9, line_type)
                mouse_flag = 2

            if key == ord("q"):
                break

            if rectangle_flag == 1:
                # cv2.rectangle(frame,(384,0),(510,128),(0,255,0),3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                # framei= frame[y:y + h, x:x + w]

            if mouse_flag == 2:
                if line_type == 'v':
                    cv2.line(frame, ((x + x + w) // 2, y), ((x + x + w) // 2, y + h), (255, 0, 0), 5)

                if line_type == 'h':
                    cv2.line(frame, (x, (y + y + h) // 2), (x + w, (y + y + h) // 2), (255, 0, 0), 5)

                # cv2.line(frame, (0, 0), (511, 511), (255, 0, 0), 5)

            cv2.putText(frame, "first press r to select ROI ..", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 200),
                        2, cv2.LINE_AA)
            cv2.putText(frame,
                        "then l to draw line..",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 200),
                        2, cv2.LINE_AA)
            cv2.putText(frame,
                        "q to quit selection mode...(DO NOT QUIT WITHOUT SELECTION) ...",
                        (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 200),
                        2, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            print_flag = 1
            #
        file1.write(str(x) + "\n")
        file1.write(str((y + y + h) // 2) + "\n")
        file1.write(str(x + w) + "\n")
        file1.write(str((y + y + h) // 2) + "\n")
        file1.write(str(line_type) + "\n")

        file1.close()


        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()


roi_creation()