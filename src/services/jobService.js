import api from "./api";

/**
 * Fetch AI recommended jobs from backend
 */
export const getRecommendedJobs = async () => {
  try {
    const response = await api.get("/recommended-jobs");
    return response.data;
  } catch (error) {
    console.error("Error fetching recommended jobs:", error);

    throw (
      error.response?.data || {
        detail: "Failed to fetch recommended jobs.",
      }
    );
  }
};

/**
 * Fetch latest jobs
 */
export const getLatestJobs = async () => {
  try {
    const response = await api.get("/latest-jobs");
    return response.data;
  } catch (error) {
    console.error("Error fetching latest jobs:", error);

    throw (
      error.response?.data || {
        detail: "Failed to fetch latest jobs.",
      }
    );
  }
};