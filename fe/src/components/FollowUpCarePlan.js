import React, { useState } from 'react';
import { Button, Card, CardContent, Dialog, DialogActions, TableHead, DialogContent, DialogTitle, Grid, Table, TableBody, TableCell, TableRow, Typography } from '@mui/material';
import ReferencesDialog from './ReferencesDialog';

const FollowUpCarePlan = ({ followUpCarePlan }) => {
  const [openDialog, setOpenDialog] = useState(false);
  const [currentReferences, setCurrentReferences] = useState([]);

  followUpCarePlan = followUpCarePlan['Follow Up Care Plan']


  console.log(followUpCarePlan)

  const handleOpenDialog = (fileNames, pageLabels, sectionKey) => {
    // Accessing context from the specific section
    console.log("sectionKey", sectionKey)
    console.log("fileNames", fileNames)
    console.log("pageLabels", pageLabels)
    const sectionContext = followUpCarePlan[sectionKey]?.context || [];
    console.log("sectionContext", sectionContext)
    const references = sectionContext.filter(contextItem =>
      fileNames.includes(contextItem.metadata.file_name) && 
      pageLabels.map(String).includes(contextItem.metadata.page_label.toString())
    );
    console.log("references", references)
    setCurrentReferences(references);
    setOpenDialog(true);
};


  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const makeEditable = (event) => {
    // Here, you would handle saving the updated content as needed
    console.log(event.target.innerText);
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
                      <Button onClick={() => handleOpenDialog(item["File names"], item["Page labels"], sectionKey)}>View References</Button>
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
                      <Button onClick={() => handleOpenDialog(item["File names"], item["Page labels"], sectionKey)}>View References</Button>
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
                      <TableCell>{item["Treatment effect"] || item["Issue"] || item["Lifestyle"] || item['Resource']}</TableCell>
                      <TableCell>{item["Explanation"]}</TableCell>
                      <TableCell>
                        <Button onClick={() => handleOpenDialog(item["File names"], item["Page labels"], sectionKey)}>View References</Button>
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
      <ReferencesDialog
        open={openDialog}
        onClose={() => setOpenDialog(false)}
        references={currentReferences}
      />
    </Grid>
  );
};

export default FollowUpCarePlan;
