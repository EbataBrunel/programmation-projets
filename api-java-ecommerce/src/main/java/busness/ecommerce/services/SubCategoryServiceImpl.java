package busness.ecommerce.services;

import busness.ecommerce.dto.SubCategoryRequestDto;
import busness.ecommerce.dto.SubCategoryResponseDto;
import busness.ecommerce.entity.Category;
import busness.ecommerce.entity.SubCategory;
import busness.ecommerce.mapper.SubCategoryMapper;
import busness.ecommerce.repository.CategoryRepository;
import busness.ecommerce.repository.SubCategoryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class SubCategoryServiceImpl implements SubCategoryService{

    private final SubCategoryRepository subCategoryRepository;
    private final CategoryRepository categoryRepository;
    private final SubCategoryMapper subCategoryMapper;

    @Override
    public SubCategoryResponseDto createSubCategory(SubCategoryRequestDto dto) {
        Category category = categoryRepository.findById(dto.getCategoryId())
                .orElseThrow(() -> new RuntimeException("Category not found"));

        SubCategory subCategory = subCategoryMapper.toEntity(dto, category);
        SubCategory subCategorySave = subCategoryRepository.save(subCategory);
        return subCategoryMapper.toDto(subCategorySave);
    }

    @Override
    public List<SubCategoryResponseDto> getAllSubCategories() {
        return subCategoryRepository.findAll()
                .stream()
                .map(subCategoryMapper::toDto)
                .toList();
    }

    @Override
    public SubCategoryResponseDto getSubCategoryById(Long id) {
        SubCategory subcategory = subCategoryRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("SubCategory not found"));
        return subCategoryMapper.toDto(subcategory);
    }

    @Override
    public List<SubCategoryResponseDto> getSubCategoriesByCategory(Long categoryId) {
        return subCategoryRepository.findByCategoryId(categoryId)
                .stream()
                .map(subCategoryMapper::toDto)
                .toList();
    }

    @Override
    public SubCategoryResponseDto updateSubCategory(Long id, SubCategoryRequestDto dto) {
        SubCategory subcategory = subCategoryRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("SubCategory not found"));

        Category category = categoryRepository.findById(dto.getCategoryId())
                .orElseThrow(() -> new RuntimeException("Category not found"));

        subcategory.setName(dto.getName());
        subcategory.setDescription(dto.getDescription());
        subcategory.setCategory(category);
        return subCategoryMapper.toDto(subCategoryRepository.save(subcategory));
    }

    @Override
    public void deleteSubCategory(Long id) {
        SubCategory subcategory = subCategoryRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("SubCategory not found"));

        subCategoryRepository.delete(subcategory);
    }
}
