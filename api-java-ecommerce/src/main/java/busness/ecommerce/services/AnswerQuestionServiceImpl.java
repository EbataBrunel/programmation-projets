package busness.ecommerce.services;

import busness.ecommerce.dto.AnswerQuestionRequestDto;
import busness.ecommerce.dto.AnswerQuestionResponseDto;
import busness.ecommerce.entity.AnswerQuestion;
import busness.ecommerce.entity.FrequentlyQuestion;
import busness.ecommerce.mapper.AnswerQuestionMapper;
import busness.ecommerce.repository.AnswerQuestionRepository;
import busness.ecommerce.repository.FrequentlyQuestionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AnswerQuestionServiceImpl implements AnswerQuestionService{

    private final AnswerQuestionRepository answerQuestionRepository;
    private final FrequentlyQuestionRepository frequentlyQuestionRepository;
    private final AnswerQuestionMapper answerQuestionMapper;

    @Override
    public AnswerQuestionResponseDto createAnswerQuestion(AnswerQuestionRequestDto dto) {
        FrequentlyQuestion frequentlyQuestion = frequentlyQuestionRepository.findById(dto.getQuestionId())
                .orElseThrow(() -> new RuntimeException("Question not found"));

        AnswerQuestion answerQuestion = answerQuestionMapper.toEntity(dto, frequentlyQuestion);
        AnswerQuestion answerQuestionSave = answerQuestionRepository.save(answerQuestion);

        return answerQuestionMapper.toDto(answerQuestionSave);
    }

    @Override
    public List<AnswerQuestionResponseDto> getAllAnswerQuestions() {
        return answerQuestionRepository.findAll()
                .stream()
                .map(answerQuestionMapper::toDto)
                .toList();
    }

    @Override
    public AnswerQuestionResponseDto getAnswerQuestionById(Long id) {
        AnswerQuestion answerQuestion = answerQuestionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Answer not found"));

        return answerQuestionMapper.toDto(answerQuestion);
    }

    @Override
    public AnswerQuestionResponseDto updateAnswerQuestion(Long id, AnswerQuestionRequestDto dto) {
        AnswerQuestion answerQuestion = answerQuestionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Answer not found"));

        FrequentlyQuestion frequentlyQuestion = frequentlyQuestionRepository.findById(dto.getQuestionId())
                .orElseThrow(() -> new RuntimeException("Question not found"));

        answerQuestion.setName(dto.getName());
        answerQuestion.setQuestion(frequentlyQuestion);

        return answerQuestionMapper.toDto(answerQuestionRepository.save(answerQuestion));
    }

    @Override
    public void deleteAnswerQuestion(Long id) {
        AnswerQuestion answerQuestion = answerQuestionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Answer not found"));

        answerQuestionRepository.delete(answerQuestion);
    }
}
