package busness.ecommerce.mapper;

import busness.ecommerce.dto.AttributeRequestDto;
import busness.ecommerce.dto.AttributeResponseDto;
import busness.ecommerce.dto.AttributeValueResponseDto;
import busness.ecommerce.entity.Attribute;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class AttributeMapper {

    public Attribute toEntity(AttributeRequestDto dto){
        return  Attribute.builder()
                .name(dto.getName())
                .build();
    }

    public AttributeResponseDto toDto(Attribute attribute) {
        return AttributeResponseDto.builder()
                .id(attribute.getId())
                .name(attribute.getName())
                .attributeValues(
                        attribute.getAttributeValues() == null
                            ? List.of()
                            :attribute.getAttributeValues()
                                .stream()
                                .map( av -> AttributeValueResponseDto.builder()
                                        .id(av.getId())
                                        .value(av.getValue())
                                        .attributeId(av.getAttribute().getId())
                                        .build())
                                .toList()

                )
                .build();
    }
}

