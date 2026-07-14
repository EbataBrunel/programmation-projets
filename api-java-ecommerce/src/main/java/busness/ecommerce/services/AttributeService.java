package busness.ecommerce.services;

import busness.ecommerce.dto.AttributeRequestDto;
import busness.ecommerce.dto.AttributeResponseDto;
import busness.ecommerce.dto.CategoryResponseDto;

import java.util.List;

public interface AttributeService {
    // CREATE
    AttributeResponseDto create(AttributeRequestDto request);

    // GET
    AttributeResponseDto getAttributeById(Long id);

    // GET
    List<AttributeResponseDto> getAll();
    // UPDATE
    AttributeResponseDto updateAttribute(Long id, AttributeRequestDto request);

    // DELETE
    void deleteAttribute(Long id);
}
