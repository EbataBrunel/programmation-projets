package busness.ecommerce.services;


import busness.ecommerce.dto.AnswerQuestionRequestDto;
import busness.ecommerce.dto.AnswerQuestionResponseDto;

import java.util.List;

public interface AnswerQuestionService {
    // CREATE
    AnswerQuestionResponseDto createAnswerQuestion(AnswerQuestionRequestDto dto);

    // READ
    List<AnswerQuestionResponseDto> getAllAnswerQuestions();

    // GET
    AnswerQuestionResponseDto getAnswerQuestionById(Long id);

    // UPDATE
    AnswerQuestionResponseDto updateAnswerQuestion(Long id, AnswerQuestionRequestDto dto);

    // DELETE
    void deleteAnswerQuestion(Long id);
}
