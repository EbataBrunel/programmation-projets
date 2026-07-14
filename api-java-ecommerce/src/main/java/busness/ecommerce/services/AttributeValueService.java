package busness.ecommerce.services;

import busness.ecommerce.dto.AttributeResponseDto;
import busness.ecommerce.dto.AttributeValueRequestDto;
import busness.ecommerce.dto.AttributeValueResponseDto;

import java.util.List;

public interface AttributeValueService {
    // CREATE
    AttributeValueResponseDto create(AttributeValueRequestDto dto);

    // GET
    List<AttributeValueResponseDto> getAll();

    // GET
    AttributeValueResponseDto getAttributeValueById(Long id);
    // GET
    List<AttributeValueResponseDto> findByAttribute(Long attributeId);
    // UPDATE
    AttributeValueResponseDto updateAttributeValue(Long id, AttributeValueRequestDto request);

    // DELETE
    void deleteAttributeValue(Long id);
}
