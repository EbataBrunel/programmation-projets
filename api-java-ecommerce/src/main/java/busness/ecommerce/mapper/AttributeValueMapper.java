package busness.ecommerce.mapper;

import busness.ecommerce.dto.AttributeValueRequestDto;
import busness.ecommerce.dto.AttributeValueResponseDto;
import busness.ecommerce.entity.AttributeValue;
import org.springframework.stereotype.Component;

@Component
public class AttributeValueMapper {



    public AttributeValueResponseDto toDto(AttributeValue attributeValue) {

        return AttributeValueResponseDto.builder()
                .id(attributeValue.getId())
                .value(attributeValue.getValue())
                .attributeId(attributeValue.getAttribute().getId())
                .attributeName(attributeValue.getAttribute().getName())
                .build();
    }
}

