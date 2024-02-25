import React from 'react';
import { AppBar, Toolbar, Typography, Container } from '@mui/material';
import HealingIcon from '@mui/icons-material/Healing';

const Header = () => {
  return (
    <AppBar position="static" color="primary" elevation={0}>
      <Container maxWidth="lg">
        <Toolbar>
          <HealingIcon sx={{ mr: 2 }} />
          <Typography variant="h6" color="inherit" noWrap>
            Medical Care Planner
          </Typography>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header;