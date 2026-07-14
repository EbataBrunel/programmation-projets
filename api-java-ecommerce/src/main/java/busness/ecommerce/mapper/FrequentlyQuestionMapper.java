package busness.ecommerce.mapper;

import busness.ecommerce.dto.AnswerQuestionResponseDto;
import busness.ecommerce.dto.FrequentlyQuestionRequestDto;
import busness.ecommerce.dto.FrequentlyQuestionResponseDto;
import busness.ecommerce.entity.FrequentlyQuestion;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class FrequentlyQuestionMapper {
    public FrequentlyQuestion toEntity(FrequentlyQuestionRequestDto dto){
        return FrequentlyQuestion.builder()
                .name(dto.getName())
                .description(dto.getDescription())
                .build();
    }

    public FrequentlyQuestionResponseDto toDto(FrequentlyQuestion question){
        return FrequentlyQuestionResponseDto.builder()
                .id(question.getId())
                .name(question.getName())
                .description(question.getDescription())
                .answers(
                        question.getAnswers() == null
                        ? List.of()
                        : question.getAnswers()
                                .stream()
                                .map(ans -> AnswerQuestionResponseDto.builder()
                                        .id(ans.getId())
                                        .name(ans.getName())
                                        .questionId(ans.getQuestion().getId())
                                        .build()
                                ).toList()
                )
                .build();
    }
}
