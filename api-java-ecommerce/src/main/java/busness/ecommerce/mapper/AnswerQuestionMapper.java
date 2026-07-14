package busness.ecommerce.mapper;

import busness.ecommerce.dto.AnswerQuestionRequestDto;
import busness.ecommerce.dto.AnswerQuestionResponseDto;
import busness.ecommerce.entity.AnswerQuestion;
import busness.ecommerce.entity.FrequentlyQuestion;
import org.springframework.stereotype.Component;

@Component
public class AnswerQuestionMapper {
    public AnswerQuestion toEntity(AnswerQuestionRequestDto dto, FrequentlyQuestion question){
        return AnswerQuestion.builder()
                .name(dto.getName())
                .question(question)
                .build();
    }

    public AnswerQuestionResponseDto toDto(AnswerQuestion answer){
        return AnswerQuestionResponseDto.builder()
                .id(answer.getId())
                .name(answer.getName())
                .questionId(answer.getQuestion().getId())
                .build();
    }
}
