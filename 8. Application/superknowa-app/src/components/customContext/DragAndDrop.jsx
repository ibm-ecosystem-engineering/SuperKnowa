import React, { useState, useRef } from "react";
import { Button, Input, Typography, LinearProgress, Link } from "@mui/material";
import { Box } from "@mui/system";
import { useDispatch, useSelector } from "react-redux";
import { upload_pdf_context } from "../../api/config";
import axios from "axios";
import { setCurrentContext } from "../../redux/currentCustomContext";
import { useNavigate } from "react-router-dom";

const DragAndDrop = () => {
  const [dragging, setDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [progress, setProgress] = useState(false);
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { paragraph } = useSelector((state) => state.currentContext);

  const handleDragEnter = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragging(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragging(false);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();
  };

  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragging(false);

    const files = event.dataTransfer.files;
    setSelectedFile(files[0]);
    // Process the dropped files here
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const uploadFile = () => {
    setProgress(true);
    const data = new FormData();
    data.append("file", selectedFile);

    axios.post(upload_pdf_context, data).then((response) => {
      dispatch(setCurrentContext(response.data.paragraph));
      setProgress(false);
      navigate("/qnacustomcontext");
    });
  };

  async function samplePdfUpload() {
    setProgress(true);
    await fetch("/sample_file_ibm_z.pdf")
      .then((response) => response.blob())
      .then((blob) => {
        let formData = new FormData();
        formData.append("file", blob, "remote-file.pdf");

        axios.post(upload_pdf_context, formData).then((response) => {
          dispatch(setCurrentContext(response.data.paragraph));
          setProgress(false);
          navigate("/qnacustomcontext");
        });
      });
  }

  return (
    <div>
      <div
        className={`drag-and-drop ${dragging ? "dragging" : ""}`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <Box
          display={"flex"}
          flexDirection={"column"}
          justifyContent={"center"}
        >
          <Typography>Drag and drop pdf file here Or</Typography>
          <Input
            type="file"
            inputProps={{ accept: "application/pdf" }}
            onChange={handleFileChange}
          />
        </Box>
      </div>
      <Box height={"50px"} display={"flex"} justifyContent={"center"}>
        {selectedFile && selectedFile.name && (
          <Typography>{selectedFile.name}</Typography>
        )}
      </Box>

      <Box sx={{ width: "100%", mt: "5px", mb: "10px" }}>
        {progress && <LinearProgress color="inherit" />}
      </Box>
      <Box display={"flex"} justifyContent={"center"} mt={"5px"}>
        <Button variant="outlined" color="inherit" onClick={uploadFile}>
          Upload
        </Button>
      </Box>
      <Box display={"flex"} justifyContent={"center"} mt={"5px"}>
        <Link href="/sample_file_ibm_z.pdf" target="_blank">
          A sample pdf file
        </Link>
      </Box>
      <Box display={"flex"} justifyContent={"center"} mt={"5px"}>
        <Button
          sx={{ width: "200px" }}
          variant="outlined"
          color="inherit"
          onClick={samplePdfUpload}
        >
          Use this sample pdf
        </Button>
      </Box>
    </div>
  );
};

export default DragAndDrop;
