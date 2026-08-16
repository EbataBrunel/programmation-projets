package eajc.group.apv.services;

import eajc.group.apv.dto.SettingRequestDto;
import eajc.group.apv.dto.SettingResponseDto;
import eajc.group.apv.entity.Setting;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.SettingMapper;
import eajc.group.apv.repository.SettingRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.UUID;

@Service
public class SettingServiceImpl implements SettingService{

    private final SettingRepository settingRepository;
    private final SettingMapper settingMapper;
    private final FileStorageService fileStorageService;

    public SettingServiceImpl(SettingRepository settingRepository, SettingMapper settingMapper, FileStorageService fileStorageService) {
        this.settingRepository = settingRepository;
        this.settingMapper = settingMapper;
        this.fileStorageService = fileStorageService;
    }

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
    public SettingResponseDto getSettingByPublicId(UUID publicId) {
        Setting setting = settingRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Setting not found"));
        return settingMapper.toDto(setting);
    }

    @Override
    public SettingResponseDto getLastSetting() {
        Setting setting = settingRepository
                .findTopByOrderByIdDesc()
                .orElseThrow(() -> new ResourceNotFoundException("No setting found"));
        return settingMapper.toDto(setting);
    }

    @Override
    public SettingResponseDto updateSetting(
            UUID publicId,
            SettingRequestDto dto,
            MultipartFile logoFile) throws IOException {
        Setting setting = settingRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Setting not found"));

        setting.setNameApp(dto.getNameApp());
        setting.setNameDev(dto.getNameDev());
        setting.setVersion(dto.getVersion());
        setting.setTheme(dto.getTheme());
        setting.setBodyTheme(dto.getBodyTheme());
        setting.setTextColor(dto.getTextColor());
        setting.setCurrency(dto.getCurrency());
        setting.setAddress(dto.getAddress());
        setting.setEmail(dto.getEmail());
        setting.setPhone(dto.getPhone());
        setting.setWidth(dto.getWidth());
        setting.setHeight(dto.getHeight());

        if (logoFile != null && !logoFile.isEmpty()) {

            // supprimer ancien logo
            if (setting.getLogo() != null && !setting.getLogo().isBlank()) {
                fileStorageService.deleteFile(setting.getLogo());
            }

            // utiliser FileStorageService
            String fileName = fileStorageService.saveFile(logoFile);
            setting.setLogo(fileName);
        }

        Setting updated = settingRepository.save(setting);

        return settingMapper.toDto(settingRepository.save(updated));
    }

    @Override
    public void deleteSetting(UUID publicId) {
        Setting setting = settingRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Setting not found"));

        // supprimer ancien logo
        if (setting.getLogo() != null && !setting.getLogo().isBlank()) {
            fileStorageService.deleteFile(setting.getLogo());
        }
        settingRepository.delete(setting);
    }
}
