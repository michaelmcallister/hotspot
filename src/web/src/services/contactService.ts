import { apiRequest } from './api';

export interface ContactData {
  [key: string]: any;
}

export const contactService = {
  async submitContact(data: ContactData): Promise<any> {
    return apiRequest('/contact', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};