import { apiRequest } from './api';

export interface StatsSummary {
  total_submissions: number;
  total_suburbs: number;
  total_postcodes: number;
  average_risk_score: number;
}

export const statsService = {
  getSummary: async (): Promise<StatsSummary> => apiRequest('/stats/summary'),
};
