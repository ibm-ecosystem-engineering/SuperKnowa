import { Grid, Typography } from "@mui/material";
import UploadFile from "../components/customContext/UploadFile";
import Footer from "../components/global/Footer";

const HomeCustomContext = () => {
  return (
    <div>
      <Grid container spacing={0} mt={"200px"}>
      <Grid item md={2}></Grid>
        <Grid item md={8} display={'flex'} justifyContent={'center'}>
         <Typography variant="h2" p={'10px'}>
            Offline version
         </Typography>
        </Grid>
        <Grid item md={2}></Grid>
        <Grid item md={2}></Grid>
        <Grid item md={8}>
          <UploadFile />
        </Grid>
        <Grid item md={2}></Grid>
      </Grid>
      <Footer/>
    </div>
  );
};

export default HomeCustomContext;
