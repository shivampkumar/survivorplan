import React from 'react';
import { Box, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, Button } from '@mui/material';

const DoctorHome = () => {
    // Dummy data for table rows
    const upcomingAppointments = [
        { patientName: 'Maria Sanchez', appointmentType: 'Chest Imaging', date: '2024-04-25' },
        { patientName: 'Michael Thompson', appointmentType: 'Blood Test', date: '2024-04-27' },
        { patientName: 'John Doe', appointmentType: 'Follow-up', date: '2024-04-30' },
        { patientName: 'Jane Smith', appointmentType: 'Follow-up', date: '2024-05-02'}
    ];

    const missedAppointments = [
        { patientName: 'Michael Thompson', appointmentType: 'Blood Test', date: '2024-03-10', notified: true },
        { patientName: 'Maria Sanchez', appointmentType: 'Chest Imaging', date: '2024-03-05', notified: false }
    ];

    const tableCellStyle = {
        fontWeight: 'bold',
        color: '#fff',
        backgroundColor: '#3d34eb' // Dark blue shade
    };

    const listItemStyle = {
        backgroundColor: '#e3f2fd', // Lighter shade of blue
        padding: '8px',
        margin: '4px 0', // Add some margin between items
        borderRadius: '4px', // Optional: if you want rounded corners
        // edit font color
        color: '#000',
    };

    const tableRowStyle = {
        '&:nth-of-type(odd)': {
            backgroundColor: '#000080', // Light blue shade for odd rows
        },
        '&:nth-of-type(even)': {
            backgroundColor: '#000080', // Even lighter blue shade for even rows
        },
        color: '#fff',
    };

    const notifyButtonStyle = {
        backgroundColor: '#d32f2f', // Red shade for Notify button
        color: '#fff',
        '&:hover': {
            backgroundColor: '#c62828',
        },
    };

    const paperStyle = {
        backgroundColor: '#000080', // Darker blue shade for Paper component
        color: '#fff',
        padding: '16px',
        marginTop: '8px',
    };

    // Render table rows
    const renderAppointmentRows = (appointments, includeNotify = false) => (
        appointments.map((appointment, index) => (
            <TableRow key={index}>
                <TableCell sx={tableRowStyle}>{appointment.patientName}</TableCell>
                <TableCell sx={tableRowStyle}>{appointment.appointmentType}</TableCell>
                <TableCell sx={tableRowStyle}>{appointment.date}</TableCell>
                {includeNotify && (
                    <TableCell sx={tableRowStyle}>
                        {appointment.notified ? 'Notified' : <Button sx={2} variant="outlined" color="primary">Notify</Button>}
                    </TableCell>
                )}
            </TableRow>
        ))
    );

    return (
        <Box sx={{ backgroundColor: 'aliceblue', padding: 2 }} display="flex" flexDirection="column" justifyContent="center" alignItems="center" p={2}>
            <Box display="flex" justifyContent="center" alignItems="flex-start" width="100%">
                <Box width="50%" p={1}>
                    <Typography variant="h6" gutterBottom>
                        Upcoming Appointments Summary
                    </Typography>
                    <TableContainer component={Paper}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell sx={tableCellStyle}>Patient Name</TableCell>
                                    <TableCell sx={tableCellStyle}>Care Action</TableCell>
                                    <TableCell sx={tableCellStyle}>Date</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {renderAppointmentRows(upcomingAppointments)}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Box>

                <Box width="50%" p={1}>
                    <Typography variant="h6" gutterBottom>
                        Missed Appointments Summary
                    </Typography>
                    <TableContainer component={Paper}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell sx={tableCellStyle} l>Patient Name</TableCell>
                                    <TableCell sx={tableCellStyle}>Appointment type</TableCell>
                                    <TableCell sx={tableCellStyle}>Date</TableCell>
                                    <TableCell sx={tableCellStyle}>Notified or Not</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {renderAppointmentRows(missedAppointments, true)}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Box>
            </Box>

            <Box width="100%" p={1}>
                <Typography variant="h6" gutterBottom>
                    SCP Summary
                </Typography>
                <Paper elevation={3} sx={{ ...paperStyle, width: '100%', padding: 2 }}>
                    <Typography>Statistics show the following:</Typography>
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                        <Box sx={listItemStyle}><li>Number of generated SCPs</li></Box>
                        <Box sx={listItemStyle}><li>Number of SCPs to be generated</li></Box>
                        <Box sx={listItemStyle}><li>Number of the SCPs were confirmed or validated by clinicians.</li></Box>
                        <Box sx={listItemStyle}><li>Number of patients without SCP</li></Box>
                        <Box sx={listItemStyle}><li>Number of SCPs that needs validation</li></Box>
                    </ul>
                </Paper>
            </Box>
        </Box>
    );
};

export default DoctorHome;