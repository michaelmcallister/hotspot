import { apiRequest } from './api';

export interface StatsSummary {
  [key: string]: any;
}

export const statsService = {
  async getSummary(): Promise<StatsSummary> {
    return apiRequest('/statistics/summary');
  },
};
