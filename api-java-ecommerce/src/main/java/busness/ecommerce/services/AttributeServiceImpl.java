package busness.ecommerce.services;

import busness.ecommerce.dto.AttributeRequestDto;
import busness.ecommerce.dto.AttributeResponseDto;
import busness.ecommerce.entity.Attribute;
import busness.ecommerce.mapper.AttributeMapper;
import busness.ecommerce.repository.AttributeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AttributeServiceImpl implements AttributeService{

    private final AttributeRepository repo;
    private final AttributeMapper attributeMapper;

    @Override
    public AttributeResponseDto create(AttributeRequestDto dto) {
        Attribute a = new Attribute();
        a.setName(dto.getName());
        return attributeMapper.toDto(repo.save(a));
    }

    @Override
    public AttributeResponseDto getAttributeById(Long id) {
        Attribute attribute = repo.findById(id)
                .orElseThrow(() -> new RuntimeException("Attribute not found"));
        return  attributeMapper.toDto(attribute);
    }

    @Override
    public List<AttributeResponseDto> getAll() {

        return repo.findAll()
                    .stream()
                    .map(attributeMapper::toDto)
                    .toList();
    }

    @Override
    public AttributeResponseDto updateAttribute(Long id, AttributeRequestDto dto) {
        Attribute attribute = repo.findById(id)
                .orElseThrow(() -> new RuntimeException("Attribute not found"));

        attribute.setName(dto.getName());
        return attributeMapper.toDto(repo.save(attribute));
    }

    @Override
    public void deleteAttribute(Long id) {
        Attribute attribute = repo.findById(id)
                .orElseThrow(() -> new RuntimeException("Attribute not found"));

        repo.delete(attribute);
    }
}
