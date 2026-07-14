package busness.ecommerce.services;

import busness.ecommerce.dto.BrandRequestDto;
import busness.ecommerce.dto.BrandResponseDto;
import busness.ecommerce.entity.Brand;
import busness.ecommerce.mapper.BrandMapper;
import busness.ecommerce.repository.BrandRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class BrandServiceImpl implements BrandService{

    private final BrandRepository brandRepository;
    private final BrandMapper brandMapper;
    @Override
    public BrandResponseDto create(BrandRequestDto request) {

        Brand brand = brandMapper.toEntity(request);
        Brand brandSave = brandRepository.save(brand);

        return brandMapper.toDto(brandSave);
    }

    @Override
    public BrandResponseDto getBrandById(Long id) {
        Brand brand = brandRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Brand not found"));
        return brandMapper.toDto(brand);
    }

    @Override
    public List<BrandResponseDto> getAll() {
        return brandRepository.findAll()
                .stream()
                .map(brandMapper::toDto)
                .toList();
    }

    @Override
    public BrandResponseDto updateBrand(Long id, BrandRequestDto request) {
        Brand brand = brandRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Brand not found"));

        brand.setName(request.getName());

        return brandMapper.toDto(brandRepository.save(brand));
    }

    @Override
    public void deleteBrand(Long id) {
        Brand brand = brandRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Brand not found"));

        brandRepository.delete(brand);
    }
}
