import React, { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Container from '@mui/material/Container';
import axios from 'axios';
import './App.css';

const App = () => {
  const [inputText, setInputText] = useState('');
  const [classification, setClassification] = useState('');

  const handleChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/api/process_data/?input=${inputText}`
      );
      setClassification(response.data.disease);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, mb: 2 }}>
        <Typography variant="h3" component="h1" align="center">
          Disease Predictor
        </Typography>
      </Box>
      <Card>
        <CardContent>
          <Box
            component="form"
            onSubmit={handleSubmit}
            sx={{
              '& > :not(style)': { mt: 2, mb: 2 },
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <TextField
              id="inputText"
              label="Enter your symptoms"
              multiline
              rows={4}
              value={inputText}
              onChange={handleChange}
              fullWidth
              required
            />
            <Button type="submit" variant="contained" color="primary">
              Submit
            </Button>
          </Box>
        </CardContent>
      </Card>
      {classification && (
        <Card sx={{ mt: 4 }}>
          <CardContent>
            <Typography variant="h5" component="h2">
              Prediction:
            </Typography>
            {classification !== 'No disease found' ? (
              <Typography variant="body1">
                You may have this condition:{' '}
                {classification.toString().toLowerCase()}
              </Typography>
            ) : (
              <Typography variant="body1">
                We were not able to determine your condition. Please add as
                many symptoms you are experiencing as possible.
              </Typography>
            )}
          </CardContent>
        </Card>
      )}
    </Container>
  );
};

export default App;