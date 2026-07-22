import api from "./api";

export const uploadResume = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post("/upload-resume", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  } catch (error) {
    console.error("Resume Upload Error:", error);

    throw (
      error.response?.data || {
        detail: "Failed to upload resume. Please try again.",
      }
    );
  }
};