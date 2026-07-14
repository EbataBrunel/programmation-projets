package busness.ecommerce.services;

import busness.ecommerce.dto.BrandRequestDto;
import busness.ecommerce.dto.BrandResponseDto;

import java.util.List;

public interface BrandService {
    // CREATE
    BrandResponseDto create(BrandRequestDto request);

    // GET
    BrandResponseDto getBrandById(Long id);

    // GET
    List<BrandResponseDto> getAll();
    // UPDATE
    BrandResponseDto updateBrand(Long id, BrandRequestDto request);

    // DELETE
    void deleteBrand(Long id);
}
