package busness.ecommerce.services;

import busness.ecommerce.dto.FrequentlyQuestionRequestDto;
import busness.ecommerce.dto.FrequentlyQuestionResponseDto;
import busness.ecommerce.entity.FrequentlyQuestion;
import busness.ecommerce.mapper.FrequentlyQuestionMapper;
import busness.ecommerce.repository.FrequentlyQuestionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class FrequentlyQuestionServiceImpl implements FrequentlyQuestionService{

    private final FrequentlyQuestionRepository frequentlyQuestionRepository;
    private final FrequentlyQuestionMapper frequentlyQuestionMapper;

    @Override
    public FrequentlyQuestionResponseDto create(FrequentlyQuestionRequestDto dto) {
        FrequentlyQuestion frequentlyQuestion = frequentlyQuestionMapper.toEntity(dto);
        FrequentlyQuestion frequentlyQuestionSave = frequentlyQuestionRepository.save(frequentlyQuestion);

        return frequentlyQuestionMapper.toDto(frequentlyQuestionSave);
    }

    @Override
    public FrequentlyQuestionResponseDto getFrequentlyQuestionById(Long id) {
        FrequentlyQuestion frequentlyQuestion = frequentlyQuestionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("FrequentlyQuestion not found"));
        return frequentlyQuestionMapper.toDto(frequentlyQuestion);
    }

    @Override
    public List<FrequentlyQuestionResponseDto> getAll() {
        return frequentlyQuestionRepository.findAll()
                .stream()
                .map(frequentlyQuestionMapper::toDto)
                .toList();
    }

    @Override
    public FrequentlyQuestionResponseDto updateFrequentlyQuestion(Long id, FrequentlyQuestionRequestDto dto) {
        FrequentlyQuestion frequentlyQuestion = frequentlyQuestionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("FrequentlyQuestion not found"));

        frequentlyQuestion.setName(dto.getName());
        frequentlyQuestion.setDescription(dto.getDescription());

        return frequentlyQuestionMapper.toDto(frequentlyQuestionRepository.save(frequentlyQuestion));
    }

    @Override
    public void deleteFrequentlyQuestion(Long id) {
        FrequentlyQuestion frequentlyQuestion = frequentlyQuestionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("FrequentlyQuestion not found"));

        frequentlyQuestionRepository.delete(frequentlyQuestion);
    }
}
