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

export const parkingService = {
  async getParkingByPostcode(postcode: string): Promise<ParkingSubmission[]> {
    return apiRequest(`/parking/${postcode}`);
  },

  async submitParking(data: any): Promise<any> {
    return apiRequest('/parking', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};