package busness.ecommerce.services;

import busness.ecommerce.dto.AttributeValueRequestDto;
import busness.ecommerce.dto.AttributeValueResponseDto;
import busness.ecommerce.entity.Attribute;
import busness.ecommerce.entity.AttributeValue;
import busness.ecommerce.mapper.AttributeValueMapper;
import busness.ecommerce.repository.AttributeRepository;
import busness.ecommerce.repository.AttributeValueRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AttributeValueServiceImpl implements AttributeValueService{

    private final AttributeValueRepository attributeValueRepository;
    private final AttributeRepository attributeRepository;
    private final AttributeValueMapper attributeValueMapper;
    @Override
    public AttributeValueResponseDto create(AttributeValueRequestDto dto) {
        Attribute attribute = attributeRepository.findById(dto.getAttributeId())
                .orElseThrow(() -> new RuntimeException("Attribute not found"));

        AttributeValue value = new AttributeValue();
        value.setValue(dto.getValue());
        value.setAttribute(attribute);

        return attributeValueMapper.toDto(attributeValueRepository.save(value));
    }

    @Override
    public List<AttributeValueResponseDto> getAll() {
        return attributeValueRepository.findAll()
                .stream()
                .map(attributeValueMapper::toDto)
                .toList();
    }

    @Override
    public AttributeValueResponseDto getAttributeValueById(Long id) {
        AttributeValue attributeValue = attributeValueRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Attribute value not found"));
        return attributeValueMapper.toDto(attributeValue);
    }

    @Override
    public List<AttributeValueResponseDto> findByAttribute(Long attributeId) {
        return attributeValueRepository.findByAttributeId(attributeId)
                .stream()
                .map(attributeValueMapper::toDto)
                .toList();
    }

    @Override
    public AttributeValueResponseDto updateAttributeValue(Long id, AttributeValueRequestDto dto) {
        AttributeValue attributeValue = attributeValueRepository.findById(id)
                .orElseThrow(()-> new RuntimeException("Attribute value not found"));

        Attribute attribute = attributeRepository.findById(dto.getAttributeId())
                .orElseThrow(() -> new RuntimeException("Attribute not found"));

        attributeValue.setValue(dto.getValue());
        attributeValue.setAttribute(attribute);

        return attributeValueMapper.toDto(attributeValueRepository.save(attributeValue));
    }

    @Override
    public void deleteAttributeValue(Long id) {
        AttributeValue attributeValue = attributeValueRepository.findById(id)
                .orElseThrow(()-> new RuntimeException("Attribute value not found"));

        attributeValueRepository.delete(attributeValue);
    }
}
