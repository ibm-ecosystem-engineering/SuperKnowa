export const profile = process.env.REACT_APP_PROFILE || "dev"
export const baseUrl=process.env.REACT_APP_BACKEND_BASE_URL || "http://localhost:3001";
export const CONTEXT_RETRIEVER=process.env.REACT_APP_CONTEXT_RETRIEVER;

export const saving_feedback_url = baseUrl + "/api/v1/feedback/add/";
export const update_feedback_url = baseUrl + "/api/v1/feedback/update/";
export const save_additional_feedback_url = baseUrl + "/api/v1/feedback/add/additional_feedback/"
export const chatBackendURL =  baseUrl + "/api/v1/chat/generate/" + CONTEXT_RETRIEVER
                                    
export const upload_pdf_context = baseUrl + "/api/v1/chat/context/upload";
export const chat_custom_context_url = baseUrl + "/api/v1/chat/context";
export const chat_multi_no_model = process.env.REACT_APP_MULTI_NO_OF_MODEL || 3
export const chat_multi_model_url = baseUrl + "/api/v1/chat/generate/multi/"+ CONTEXT_RETRIEVER +"/"+chat_multi_no_model;
