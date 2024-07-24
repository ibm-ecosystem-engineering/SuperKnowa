import { baseUrl, saving_feedback_url, update_feedback_url } from "../config";
import axios from "axios";

/*
  Save star Ranking drag and drop
*/
export const saveMultiFeedback = (
  rankingValues,
  reference_id,
  answerValues,
  ratingValues,
  feedbackReference_id,
  setFeedbackReference,
  question
) => {
  // Getting the mongo reference id to link up with feedback pipeline
  if (!reference_id) {
    return;
  }
  const feedback = construct_multi_feedback_saving_object(
    rankingValues,
    answerValues,
    ratingValues,
    question
  );

  if (feedbackReference_id) {
    // its an update
    updateFeedback(feedback, feedbackReference_id);
  } else {
    // its an insert
    SaveFeedback(feedback, reference_id, setFeedbackReference);
  }
};

/*
  Save star rating
*/
export const saveRating = (
  rating,
  reference_id,
  feedbackReference,
  setFeedbackReference
) => {
  if (!rating) {
    return;
  }

  if (feedbackReference) {
    // its an update
    updateFeedback(rating, feedbackReference);
  } else {
    // its an insert
    SaveFeedback(rating, reference_id, setFeedbackReference);
  }
};

/* Save feedbak from additional window */
export const additionalFeedback = (
  feedback,
  reference_id,
  feedbackReference,
  setFeedbackReference
) => {
  if (!feedback) return;

  if (feedbackReference) {
    // its an update
    updateFeedback(feedback, feedbackReference);
  } else {
    // its an insert
    SaveFeedback(feedback, reference_id, setFeedbackReference);
  }
};

/* Multi model Save feedbak from additional window */
export const multiAdditionalFeedback = (
  feedback,
  reference_id,
  feedbackReference,
  setFeedbackReference
) => {
  if (!feedback) return;

  if (feedbackReference) {
    // its an update
    axios
      .post(
        baseUrl + "/api/v1/feedback/add/multi_additional/" + feedbackReference,
        feedback
      )
      .then((response) => {
      })
      .catch((error) => {
        console.error(error);
      });
  } else {
    // its an insert
    SaveFeedback(feedback, reference_id, setFeedbackReference);
  }
};

/* Offline version of feedback saving */
export const saveOfflineFeedback = (
  feedback,
  reference_id,
  feedbackReference,
  setFeedbackReference
) => {
  if (!feedback) {
    return;
  }

  if (feedbackReference) {
    // its an update
  } else {
    // its an insert
  }
};

/* update feedback generic method */
const updateFeedback = (feedback, feedbackReference_id) => {
  axios
    .post(update_feedback_url + feedbackReference_id, feedback)
    .then((response) => {
    })
    .catch((error) => {
      console.error(error);
    });
};

/* generic feedback saving */

export const SaveFeedback = (feedback, reference_id, setFeedbackReference) => {
  if (!reference_id) return;
  axios
    .put(saving_feedback_url + reference_id, feedback)
    .then((response) => {
      setFeedbackReference(response.data.feedback_ref);
    })
    .catch((error) => {
      console.error(error);
    });
};

const construct_multi_feedback_saving_object = (
  rankingValues,
  answerValues,
  ratingValues,
  question
) => {
  var rankig = rankingValues.map((item, index) => {
    return {
      rank: index,
      model_id: item.model_id,
    };
  });

  var answers = answerValues.map((item, index) => {
    return {
      model_id: item.model_id,
      answer: item.answer,
    };
  });

  return {
    feedbackDate: new Date().toISOString(),
    type: "multi_model",
    answers: answers,
    question: question,
    rankig: rankig,
    rating: ratingValues,
  };
};
