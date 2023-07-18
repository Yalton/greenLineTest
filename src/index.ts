import express from 'express';
import { Request, Response, NextFunction } from 'express';
import axios from 'axios';
import multer from 'multer';
const upload = multer();
import { v4 as uuidv4 } from 'uuid';

const app = express();
app.use(express.json());
app.use(express.static('public'));

interface QueueItem {
    req: Request;
    res: Response;
    next: NextFunction;
    downloadId: string;
}

interface DownloadStatus {
    status: 'queued' | 'processing' | 'completed' | 'error';
    downloadUrl?: string;
    message?: string;
}

let isProcessing = false;
let queue: QueueItem[] = [];
const downloads: Record<string, DownloadStatus> = {};
const port = 3000;

app.post("/predict", upload.single('image'), async (req: Request, res: Response) => {
    if (req.file) {
        const file = req.file;  // Assuming you're using multer or a similar middleware
        // Convert the file to base64
        const base64_image = file.buffer.toString('base64');

        try {
            const fastApiRes = await axios.post('http://127.0.0.1:8000/predict', { base64_image });

            // Send back the base64 image from the FastAPI server
            res.json({ base64_image: fastApiRes.data.base64_image });
        } catch (err) {
            console.error("Error Calling to the FastAPI backend:", (err as any).response ? (err as any).response : err)
        }
    } else {
        res.status(400).send("No file uploaded.");
    }
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});