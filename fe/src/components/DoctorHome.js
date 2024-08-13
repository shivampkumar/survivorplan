import React from 'react';
import './DoctorHome.css';
import { Box, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, Button } from '@mui/material';

const DoctorHome = () => {
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
        color: '#FFC107', // Consistent yellow text for headings
        backgroundColor: '#282828', // Dark background for table headings
        border: '1px solid #444', // Border for table cells
    };

    const listItemStyle = {
        backgroundColor: '#333333', // Darker shade of grey for list items
        padding: '8px',
        margin: '4px 0',
        borderRadius: '4px',
        color: '#FFFFFF', // White text
    };

    const tableRowStyle = {
        '&:nth-of-type(odd)': {
            backgroundColor: '#2C2C2C', // Dark grey shade for odd rows
        },
        '&:nth-of-type(even)': {
            backgroundColor: '#333333', // Even darker shade for even rows
        },
        color: '#FFFFFF', // White text
        border: '1px solid #444', // Border for table rows
    };

    const notifyButtonStyle = {
        backgroundColor: '#d32f2f', // Red shade for Notify button
        color: '#FFFFFF', // White text
        '&:hover': {
            backgroundColor: '#c62828',
        },
    };

    const paperStyle = {
        backgroundColor: '#2B2B2B', // Slightly lighter dark background for Paper component
        color: '#FFFFFF', // White text
        padding: '16px',
        marginTop: '8px',
        border: '1px solid #444', // Border for paper
        borderRadius: '8px', // Rounded corners for paper
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)', // Subtle shadow for depth
    };

    const renderAppointmentRows = (appointments, includeNotify = false) => (
        appointments.map((appointment, index) => (
            <TableRow key={index} sx={tableRowStyle}>
                <TableCell>{appointment.patientName}</TableCell>
                <TableCell>{appointment.appointmentType}</TableCell>
                <TableCell>{appointment.date}</TableCell>
                {includeNotify && (
                    <TableCell>
                        {appointment.notified ? 'Notified' : <Button sx={notifyButtonStyle} variant="outlined">Notify</Button>}
                    </TableCell>
                )}
            </TableRow>
        ))
    );

    return (
        <Box sx={{ backgroundColor: '#1A1A1A', padding: 2, minHeight: '100vh', border: '1px solid #444', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)' }} display="flex" flexDirection="column" alignItems="center">
            <Box display="flex" justifyContent="center" alignItems="flex-start" width="100%" sx={{ backgroundColor: '#1E1E1E', padding: 2, borderRadius: '8px' }}>
                <Box width="50%" p={1}>
                    <Typography variant="h6" gutterBottom sx={{ color: '#FFC107' }}>
                        Upcoming Appointments Summary
                    </Typography>
                    <TableContainer component={Paper} sx={paperStyle}>
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
                    <Typography variant="h6" gutterBottom sx={{ color: '#FFC107' }}>
                        Missed Appointments Summary
                    </Typography>
                    <TableContainer component={Paper} sx={paperStyle}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell sx={tableCellStyle}>Patient Name</TableCell>
                                    <TableCell sx={tableCellStyle}>Appointment Type</TableCell>
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
                <Typography variant="h6" gutterBottom sx={{ color: '#FFC107' }}>
                    SCP Summary
                </Typography>
                <Paper elevation={3} sx={paperStyle}>
                    <Typography>Statistics show the following:</Typography>
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                        <Box sx={listItemStyle}><li>Number of generated SCPs</li></Box>
                        <Box sx={listItemStyle}><li>Number of SCPs to be generated</li></Box>
                        <Box sx={listItemStyle}><li>Number of SCPs were confirmed or validated by clinicians.</li></Box>
                        <Box sx={listItemStyle}><li>Number of patients without SCP</li></Box>
                        <Box sx={listItemStyle}><li>Number of SCPs that need validation</li></Box>
                    </ul>
                </Paper>
            </Box>
        </Box>
    );
};

export default DoctorHome;
