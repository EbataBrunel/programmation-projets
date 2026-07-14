package busness.ecommerce.services;

import busness.ecommerce.dto.FrequentlyQuestionRequestDto;
import busness.ecommerce.dto.FrequentlyQuestionResponseDto;
import busness.ecommerce.entity.FrequentlyQuestion;

import java.util.List;

public interface FrequentlyQuestionService {
    // CREATE
    FrequentlyQuestionResponseDto create(FrequentlyQuestionRequestDto dto);

    // GET
    FrequentlyQuestionResponseDto getFrequentlyQuestionById(Long id);

    // GET
    List<FrequentlyQuestionResponseDto> getAll();
    // UPDATE
    FrequentlyQuestionResponseDto updateFrequentlyQuestion(Long id, FrequentlyQuestionRequestDto dto);

    // DELETE
    void deleteFrequentlyQuestion(Long id);
}
