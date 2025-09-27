import { apiRequest } from './api';

export interface Address {
  address: string;
  suburb: string;
  postcode: string;
}

export const addressService = {
  getAddresses: async (postcode: string, query?: string): Promise<Address[]> => {
    const url = query
      ? `/addresses/${postcode}?q=${encodeURIComponent(query)}`
      : `/addresses/${postcode}`;
    return apiRequest(url);
  },
};
