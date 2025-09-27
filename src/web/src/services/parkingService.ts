import { apiRequest } from './api';

export interface ParkingSubmission {
  parking_id: number;
  address: string;
  suburb: string;
  postcode: string;
  type: string;
  lighting: number | null;
  cctv: boolean | null;
  created_at: string;
  facilities: Array<{
    facility_id: number;
    facility_name: string;
  }>;
}

export interface ParkingSubmissionData {
  address: string;
  suburb: string;
  postcode: string;
  type: string;
  lighting: number | null;
  cctv: boolean | null;
  facilities: number[];
}

export interface SubmissionResponse {
  success: boolean;
  parking_id?: number;
  message: string;
}

export const parkingService = {
  getParkingByPostcode: async (postcode: string): Promise<ParkingSubmission[]> =>
    apiRequest(`/parking/${postcode}`),

  submitParking: async (data: ParkingSubmissionData): Promise<SubmissionResponse> => apiRequest('/parking', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};
