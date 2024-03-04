import React, { useState } from 'react';
import { Button, Card, CardContent, Dialog, DialogActions,TableHead, DialogContent, DialogTitle, Grid, Table, TableBody, TableCell, TableRow, Typography } from '@mui/material';

const FollowUpCarePlan = ({ followUpCarePlan }) => {
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogContent, setDialogContent] = useState([]);
  followUpCarePlan = followUpCarePlan['Follow Up Care Plan']
  console.log(followUpCarePlan)
  // Function to handle opening the dialog for references
  const handleOpenDialog = (fileNames, pageLabels) => {
    setDialogContent(fileNames.map((fileName, index) => ({
      fileName,
      pageLabel: pageLabels[index]
    })));
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  return (
    <Grid container spacing={2}>
      {/* Display cancer_type and patient_data */}
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6">Cancer Type</Typography>
            <Typography>{followUpCarePlan["cancer_type"]}</Typography>
          </CardContent>
        </Card>
      </Grid>
      {/* <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6">Patient Data</Typography>
            <Typography>{followUpCarePlan["patient_data"]}</Typography>
          </CardContent>
        </Card>
      </Grid> */}

      {/* Render other sections in a table format */}
      {Object.keys(followUpCarePlan).filter(key => ['Schedule of Clinical Visits'].includes(key)).map((sectionKey) => (
        <Grid item xs={12} key={sectionKey}>
          <Card>
            <CardContent>
              <Typography variant="h6">{sectionKey}</Typography>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Visit Type</TableCell>
                    <TableCell>When/How Often</TableCell>
                    <TableCell>Explanation</TableCell>
                    <TableCell>References</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {followUpCarePlan[sectionKey].recommendation[sectionKey].map((item, index) => (
                    <TableRow key={index}>
                      <TableCell>{item["Visit type"] || item["Test type"]}</TableCell>
                      <TableCell>{item["When / how often"]}</TableCell>
                      <TableCell>{item["Explanation"]}</TableCell>
                      <TableCell>
                        <Button onClick={() => handleOpenDialog(item["File names"], item["Page labels"])}>View References</Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </Grid>
      ))}

    {Object.keys(followUpCarePlan).filter(key => ['Cancer Surveillance or Other Recommended Tests'].includes(key)).map((sectionKey) => (
            <Grid item xs={12} key={sectionKey}>
            <Card>
                <CardContent>
                <Typography variant="h6">{sectionKey}</Typography>
                <Table>
                    <TableHead>
                    <TableRow>
                        <TableCell>Test Type</TableCell>
                        <TableCell>Coordinating Provider</TableCell>
                        <TableCell>When/How Often</TableCell>
                        <TableCell>Explanation</TableCell>
                        <TableCell>References</TableCell>
                    </TableRow>
                    </TableHead>
                    <TableBody>
                    {followUpCarePlan[sectionKey].recommendation[sectionKey].map((item, index) => (
                        <TableRow key={index}>
                        <TableCell>{item["Visit type"] || item["Test type"]}</TableCell>
                        <TableCell>{item["Coordinating provider"]}</TableCell>
                        <TableCell>{item["When / how often"]}</TableCell>
                        <TableCell>{item["Explanation"]}</TableCell>
                        <TableCell>
                            <Button onClick={() => handleOpenDialog(item["File names"], item["Page labels"])}>View References</Button>
                        </TableCell>
                        </TableRow>
                    ))}
                    </TableBody>
                </Table>
                </CardContent>
            </Card>
            </Grid>
        ))}

    {Object.keys(followUpCarePlan).filter(key => ['Possible late and long-term effects of cancer treatment', 'Other issues', 'Lifestyle and behavior', 'Helpful resources'].includes(key)).map((sectionKey) => (
            <Grid item xs={12} key={sectionKey}>
            <Card>
                <CardContent>
                <Typography variant="h6">{sectionKey}</Typography>
                <Table>
                    <TableHead>
                    <TableRow>
                        <TableCell>Treatment effect</TableCell>
                        <TableCell>Explanation</TableCell>
                        <TableCell>References</TableCell>
                    </TableRow>
                    </TableHead>
                    <TableBody>
                    {followUpCarePlan[sectionKey].recommendation[sectionKey].map((item, index) => (
                        <TableRow key={index}>
                        <TableCell>{item["Treatment effect"] || item["Issue"] || item["Lifestyle"]|| item['Resource']}</TableCell>
                        <TableCell>{item["Explanation"]}</TableCell>
                        <TableCell>
                            <Button onClick={() => handleOpenDialog(item["File names"], item["Page labels"])}>View References</Button>
                        </TableCell>
                        </TableRow>
                    ))}
                    </TableBody>
                </Table>
                </CardContent>
            </Card>
            </Grid>
        ))}

      {/* Dialog for displaying references */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>References</DialogTitle>
        <DialogContent>
          {dialogContent.map((content, index) => (
            <Typography key={index}>
              <a href={`/path/to/files/${content.fileName}#page=${content.pageLabel}`} target="_blank" rel="noopener noreferrer">
                {content.fileName} - Page {content.pageLabel}
              </a>
            </Typography>
          ))}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Close</Button>
        </DialogActions>
      </Dialog>
    </Grid>
  );
};

export default FollowUpCarePlan;
