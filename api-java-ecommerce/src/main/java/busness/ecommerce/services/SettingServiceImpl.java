package busness.ecommerce.services;

import busness.ecommerce.dto.SettingRequestDto;
import busness.ecommerce.dto.SettingResponseDto;
import busness.ecommerce.entity.Setting;
import busness.ecommerce.mapper.SettingMapper;
import busness.ecommerce.repository.SettingRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

@Service
@RequiredArgsConstructor
public class SettingServiceImpl implements SettingService{

    private final SettingRepository settingRepository;
    private final SettingMapper settingMapper;
    private final FileStorageService fileStorageService;

    @Override
    public SettingResponseDto createSetting(SettingRequestDto dto, MultipartFile logoFile) throws IOException {
        String fileName = fileStorageService.saveFile(logoFile);

        Setting setting = settingMapper.toEntity(dto, fileName);
        Setting settingSave = settingRepository.save(setting);
        return settingMapper.toDto(settingSave);
    }

    @Override
    public List<SettingResponseDto> getAllSetting() {
        return settingRepository.findAll()
                .stream()
                .map(settingMapper::toDto)
                .toList();
    }

    @Override
    public SettingResponseDto getSettingById(Long id) {
        Setting setting = settingRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Setting not found"));
        return settingMapper.toDto(setting);
    }

    @Override
    public SettingResponseDto getLastSetting() {
        Setting setting = settingRepository
                .findTopByOrderByIdDesc()
                .orElseThrow(() -> new RuntimeException("No setting found"));
        return settingMapper.toDto(setting);
    }

    @Override
    public SettingResponseDto updateSetting(
            Long id,
            SettingRequestDto dto,
            MultipartFile logoFile) throws IOException {
        Setting setting = settingRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Setting not found"));

        setting.setNameApp(dto.getNameApp());
        setting.setNameDev(dto.getNameDev());
        setting.setVersion(dto.getVersion());
        setting.setTheme(dto.getTheme());
        setting.setTextColor(dto.getTextColor());
        setting.setCurrency(dto.getCurrency());
        setting.setAddress(dto.getAddress());
        setting.setEmail(dto.getEmail());
        setting.setPhone(dto.getPhone());
        setting.setWidth(dto.getWidth());
        setting.setHeight(dto.getHeight());

        if (logoFile != null && !logoFile.isEmpty()) {

            // supprimer ancien logo
            if (setting.getLogo() != null) {
                Path oldPath = Paths.get("uploads/" + setting.getLogo());
                Files.deleteIfExists(oldPath);
            }

            // utiliser FileStorageService
            String fileName = fileStorageService.saveFile(logoFile);
            setting.setLogo(fileName);
        }

        Setting updated = settingRepository.save(setting);

        return settingMapper.toDto(settingRepository.save(updated));
    }

    @Override
    public void deleteSetting(Long id) {
        Setting setting = settingRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Setting not found"));

        settingRepository.delete(setting);
    }
}
