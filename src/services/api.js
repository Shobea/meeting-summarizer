//api service for meeting summarizer
//handles all communication with the python backend

import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 300000, //5 minutes - ml processing can take time
});

//check if the backend is running
export async function checkHealth() {
  const response = await api.get('/health');
  return response.data;
}

//transcribe an audio file to text
//audioBlob: the audio file to transcribe
//returns: {text: string, language: string}
export async function transcribeAudio(audioBlob) {
  const formData = new FormData();
  formData.append('file', audioBlob, 'recording.webm');
  
  const response = await api.post('/transcribe', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
}

//summarize text
//text: the text to summarize
//options.maxLength: maximum summary length (default: 150)
//options.minLength: minimum summary length (default: 30)
//returns: {summary: string, original_length: number, summary_length: number}
export async function summarizeText(text, options = {}) {
  const response = await api.post('/summarize', {
    text,
    max_length: options.maxLength || 150,
    min_length: options.minLength || 30,
  });
  
  return response.data;
}

//process a complete meeting: transcribe audio and summarize
//this is the main function to use when ending a meeting
//audioBlob: the recorded audio
//returns: {meeting_id: string, transcription: string, summary: string, language: string, processed_at: string}
export async function processMeeting(audioBlob) {
  const formData = new FormData();
  formData.append('file', audioBlob, 'meeting-recording.webm');
  
  const response = await api.post('/process-meeting', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
}

//preload ml models in the background (optional, speeds up first request)
export async function preloadModels() {
  const response = await api.post('/preload-models');
  return response.data;
}

export default {
  checkHealth,
  transcribeAudio,
  summarizeText,
  processMeeting,
  preloadModels,
};
