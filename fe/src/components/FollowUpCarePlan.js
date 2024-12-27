import React, { useState } from 'react';
import { Card, CardContent, Grid, Table, TableBody, IconButton, TableCell, TableHead, TableRow, Typography, Checkbox } from '@mui/material';
import ReferencesDialog from './ReferencesDialog';
import InfoIcon from '@mui/icons-material/Info';
import './FollowUpCarePlan.css';

const FollowUpCarePlan = ({ data }) => {
  const [openDialog, setOpenDialog] = useState(false);
  const [currentReferences, setCurrentReferences] = useState([]);
  const [verifiedRows, setVerifiedRows] = useState({});

  if (!data) return <div>Loading...</div>;

  const handleOpenDialog = (contextId, sectionKey) => {
    const contextKey = `retrieved_context_${sectionKey}`;
    const references = data[contextKey]?.retrieved_context[contextId] || [];
    setCurrentReferences(references);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleVerificationChange = (path) => {
    setVerifiedRows(prev => ({
      ...prev,
      [path]: !prev[path]
    }));
  };

  const renderSymptomsSection = (followUpData) => {
    const symptoms = followUpData["Already Experienced Symptoms"]?.symptoms;
    console.log("Already Experienced Symptoms", followUpData["Already Experienced Symptoms"]);
    if (!symptoms) return null;
    
    return (
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Question</TableCell>
            <TableCell>Answer</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>Already experienced symptoms or side effects?</TableCell>
            <TableCell>{symptoms}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    );
  };

  const renderSurveillanceSection = (followUpData) => {
    const tests = followUpData["Cancer Surveillance"]?.tests;
    console.log("Cancer Surveillance tests:", tests);

    if (!tests) {
      console.log("No tests found");
      return null;
    }

    return (
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Test Type</TableCell>
            <TableCell>When/How Often</TableCell>
            <TableCell>Frequency (weeks)</TableCell>
            <TableCell>Explanation</TableCell>
            <TableCell>References</TableCell>
            <TableCell>Verify</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {tests.map((test, index) => (
            <TableRow key={index}>
              <TableCell>{test["Test type"]}</TableCell>
              <TableCell>{test["When / how often"]}</TableCell>
              <TableCell>{test["Frequency (in weeks)"]}</TableCell>
              <TableCell>{test["Explanation"]}</TableCell>
              <TableCell>
                {test.references && (
                  <IconButton onClick={() => handleOpenDialog(test["Retrieved context id"], "Cancer surveillance and other recommended tests for cancer monitoring")}>
                    <InfoIcon />
                  </IconButton>
                )}
              </TableCell>
              <TableCell>
                <Checkbox
                  checked={verifiedRows[`surveillance-${index}`] || false}
                  onChange={() => handleVerificationChange(`surveillance-${index}`)}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    );
  };

  const renderLifestyleSection = (followUpData) => {
    const lifestyleRecs = followUpData["Lifestyle Recommendations"]?.recommendations || [];
    const recommendations = [...lifestyleRecs];
    if (!recommendations.length) return null;

    return (
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Lifestyle</TableCell>
            <TableCell>Explanation</TableCell>
            <TableCell>References</TableCell>
            <TableCell>Verify</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {recommendations.map((rec, index) => (
            <TableRow key={index}>
              <TableCell>{rec["Lifestyle"]}</TableCell>
              <TableCell>{rec["Explanation"]}</TableCell>
              <TableCell>
                {rec.references && (
                  <IconButton onClick={() => handleOpenDialog(rec["Retrieved context id"], "Lifestyle and behavior recommendations for cancer survivors")}>
                    <InfoIcon />
                  </IconButton>
                )}
              </TableCell>
              <TableCell>
                <Checkbox
                  checked={verifiedRows[`lifestyle-${index}`] || false}
                  onChange={() => handleVerificationChange(`lifestyle-${index}`)}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    );
  };

  const renderEffectsSection = (followUpData) => {
    const effects = followUpData["Late and Long-term Effects"]?.effects;
    if (!effects || !Array.isArray(effects)) return null;

    return (
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Treatment Effect</TableCell>
            <TableCell>Explanation</TableCell>
            <TableCell>References</TableCell>
            <TableCell>Verify</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {effects.map((effect, index) => (
            <TableRow key={index}>
              <TableCell>{effect["Treatment effect"]}</TableCell>
              <TableCell>{effect["Explanation"]}</TableCell>
              <TableCell>
                <IconButton onClick={() => handleOpenDialog(effect["Retrieved context id"], "Possible late and long-term effects of cancer treatment")}>
                  <InfoIcon />
                </IconButton>
              </TableCell>
              <TableCell>
                <Checkbox
                  checked={verifiedRows[`effects-${index}`] || false}
                  onChange={() => handleVerificationChange(`effects-${index}`)}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    );
  };

  const renderIssuesSection = (followUpData) => {
    const issues = followUpData["Other Issues"]?.issues;
    if (!issues || !Array.isArray(issues)) return null;

    return (
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Issue</TableCell>
            <TableCell>Explanation</TableCell>
            <TableCell>References</TableCell>
            <TableCell>Verify</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {issues.map((issue, index) => (
            <TableRow key={index}>
              <TableCell>{issue["Issue"]}</TableCell>
              <TableCell>{issue["Explanation"]}</TableCell>
              <TableCell>
                <IconButton onClick={() => handleOpenDialog(issue["Retrieved context id"], "Possible other issues that cancer survivors may experience")}>
                  <InfoIcon />
                </IconButton>
              </TableCell>
              <TableCell>
                <Checkbox
                  checked={verifiedRows[`issues-${index}`] || false}
                  onChange={() => handleVerificationChange(`issues-${index}`)}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    );
  };

  const renderResourcesSection = (followUpData) => {
    const resources = followUpData["Helpful Resources"]?.resources;
    if (!resources || !Array.isArray(resources)) return null;

    return (
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Resource</TableCell>
            <TableCell>Explanation</TableCell>
            <TableCell>References</TableCell>
            <TableCell>Verify</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {resources.map((resource, index) => (
            <TableRow key={index}>
              <TableCell>{resource["Resource"]}</TableCell>
              <TableCell>{resource["Explanation"]}</TableCell>
              <TableCell>
                <IconButton onClick={() => handleOpenDialog(resource["Retrieved context id"], "References to helpful resources for cancer survivors")}>
                  <InfoIcon />
                </IconButton>
              </TableCell>
              <TableCell>
                <Checkbox
                  checked={verifiedRows[`resources-${index}`] || false}
                  onChange={() => handleVerificationChange(`resources-${index}`)}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    );
  };

  return (
    <div className="follow-up-care-plan-container">
      <Typography variant="h4" className="follow-up-care-plan-title">
        Follow-up Care Plan
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6">Already Experienced Symptoms</Typography>
              {renderSymptomsSection(data)}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6">Cancer Surveillance</Typography>
              {renderSurveillanceSection(data)}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6">Lifestyle Recommendations</Typography>
              {renderLifestyleSection(data)}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6">Late and Long-term Effects</Typography>
              {renderEffectsSection(data)}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6">Other Issues</Typography>
              {renderIssuesSection(data)}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6">Helpful Resources</Typography>
              {renderResourcesSection(data)}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <ReferencesDialog
        open={openDialog}
        onClose={handleCloseDialog}
        references={currentReferences}
      />
    </div>
  );
};

export default FollowUpCarePlan;
