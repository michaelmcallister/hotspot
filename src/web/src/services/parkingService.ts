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
    // Fetch the postcode feed and return only the parking submissions list
    const feed = await apiRequest<any>(`/postcode/${postcode}/feed`);
    return Array.isArray(feed?.parking_submissions) ? feed.parking_submissions : [];
  },

  async submitParking(data: any): Promise<any> {
    return apiRequest('/parking', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};
