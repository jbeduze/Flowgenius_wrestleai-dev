import streamlit as st
import cv2
import tempfile
import numpy as np
import os
from streamlit_extras.stylable_container import stylable_container

def get_frame(cap, frame_number):
    """Seek to the specified frame number and return the frame."""
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    else:
        frame = None  # None indicates an invalid frame
    return frame

st.title('Video Analysis')

col1, col2 = st.columns([1, 1])

with col1:
    video_file_buffer = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi", "mkv"])

with col2:
    with st.popover("How to use this page"):
        st.write("""
        ## How to Use This Page

        1. **Upload a Video**: Click on the "Upload a Video" button to select and upload your video file (supported formats: mp4, mov, avi, mkv).
        2. **Select Frame Range**: Use the slider to select the range of frames you want to analyze.
        3. **View Frames**: The selected frames and their surrounding frames will be displayed in the columns below.
        4. **Create Downloadable Video Segment**: Click the "Create downloadable video segment" button to extract and download the selected segment of the video.
        5. **Use Current Video Segment Selection**: Click on the "Use current video segment selection" to provide additional notes and submit the segment for processing.
        6. **Submit for Processing**: Enter any notes in the text area and click the "Submit for Processing" button to send your video segment for further analysis.
        """)

if video_file_buffer is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file_buffer.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if 'frame_range' not in st.session_state or not st.session_state.frame_range:
        st.session_state.frame_range = (0, min(10, total_frames - 1))

    frame_range = st.slider(
        'Select Frame Range',
        0, total_frames - 1,
        st.session_state.frame_range,
        key='frame_range'
    )

    # Display selected frame range and surrounding frames
    col1, col2, col3 = st.columns([1,2,1])
    frames_to_display = [
        (frame_range[0] - 1, "**Frame Before Start, not included in segment selected**"),
        (frame_range[0], "Start Frame"),
        (frame_range[1], "End Frame"),
        (frame_range[1] + 1, "Frame After End, not included in segment selected")
    ]

    with col1:
        def before_video_segment_container():
                with stylable_container(
                    key="before_video_segment_container",
                    css_styles="""
                    {
                        background-color: #708090CC;
                       
                        border: 2px solid #FFCB05;
                        border-radius: 5px;
                        box-shadow: 0px 0px 15px 3px #C40000;
                        padding: 5px;
                    }
                    """,
                ):
                    with st.container():
                        frame_index, label = frames_to_display[0]
                        if 0 <= frame_index < total_frames:
                            frame = get_frame(cap, frame_index)
                            if frame is not None:
                                st.image(frame)
                                st.caption(f"{label} {frame_index}")
                            else:
                                st.write("No frame available")
                        else:
                            st.write("No frame available")
        before_video_segment_container()
    with col2:
        def video_segment_container():
                with stylable_container(
                    key="video_segment_container",
                    css_styles="""
                    {
                        background-color: #708090CC;
                       
                        border: 2px solid #FFCB05;
                        border-radius: 5px;
                        box-shadow: 0px 0px 15px 3px #4FF73A;
                        padding: 5px;
                    }
                    """,
                ):
                    with st.container():
                        subcol1, subcol2 = st.columns(2)
                        with subcol1:
                            frame_index, label = frames_to_display[1]
                            if 0 <= frame_index < total_frames:
                                frame = get_frame(cap, frame_index)
                                if frame is not None:
                                    st.image(frame)
                                    st.caption(f"{label} {frame_index}")
                                else:
                                    st.write("No frame available")
                            else:
                                st.write("No frame available")
                        with subcol2:
                            frame_index, label = frames_to_display[2]
                            if 0 <= frame_index < total_frames:
                                frame = get_frame(cap, frame_index)
                                if frame is not None:
                                    st.image(frame)
                                    st.caption(f"{label} {frame_index}")
                                else:
                                    st.write("No frame available")
                            else:
                                st.write("No frame available")
        video_segment_container()
    with col3:
        def after_video_segment_container():
                with stylable_container(
                    key="after_video_segment_container",
                    css_styles="""
                    {
                        background-color: #708090CC;
                       
                        border: 2px solid #FFCB05;
                        border-radius: 5px;
                        box-shadow: 0px 0px 15px 3px #C40000;
                        padding: 5px;
                    }
                    """,
                ):
                    with st.container():
                        frame_index, label = frames_to_display[3]
                        if 0 <= frame_index < total_frames:
                            frame = get_frame(cap, frame_index)
                            if frame is not None:
                                st.image(frame)
                                st.caption(f"{label} {frame_index}")
                            else:
                                st.write("No frame available")
                        else:
                            st.write("No frame available")
        after_video_segment_container()
    # Extract and download video segment
    if st.button("Create downloadable video segment"):
        # Setting up video writer
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0])
        output_file_path = tempfile.mktemp(suffix='.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(output_file_path, fourcc, out_fps, (frame_width, frame_height))

        for _ in range(frame_range[0], frame_range[1] + 1):
            ret, frame = cap.read()
            if ret:
                out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))  # Writing frame to output file

        out.release()
        cap.release()

        # Download link
        with open(output_file_path, 'rb') as f:
            st.download_button('Confirm download', f, file_name='video_segment.mp4')

        os.remove(output_file_path)  # Clean up temporary file

    # Popover for processing the selected segment
    with st.expander("Use current video segment selection"):
        st.markdown(f"**Ready to process frames: {frame_range}**")
        user_notes = st.text_area("User Notes", "")
        if st.button("Submit for Processing"):
            st.write("Your video segment has been submitted for processing!")
            st.write(f"Frame Range: {frame_range}")
            st.write(f"User Notes: {user_notes}")

else:
    st.text("Please upload a video file to proceed.")
