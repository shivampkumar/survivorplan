import React from 'react';
import { AppBar, Toolbar, Typography, Container } from '@mui/material';
import HealingIcon from '@mui/icons-material/Healing';


const Header = () => {
  return (
    <AppBar position="static" color="navyBlue" elevation={0} className='appbar'>
      <Container maxWidth="lg">
        <Toolbar>
          <HealingIcon sx={{ mr: 2 }} />
          <Typography variant="h6" color="inherit" noWrap>
           Survivorship Navigator
          </Typography>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header;