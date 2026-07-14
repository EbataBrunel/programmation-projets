package busness.ecommerce.services;

import busness.ecommerce.dto.UserProfileRequestDto;
import busness.ecommerce.dto.UserProfileResponseDto;
import busness.ecommerce.entity.Setting;
import busness.ecommerce.entity.UserProfile;
import busness.ecommerce.entity.User;
import busness.ecommerce.mapper.UserProfileMapper;
import busness.ecommerce.repository.ClientRepository;
import busness.ecommerce.repository.UserRepository;
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
public class UserProfileServiceImpl implements UserProfileService {

    private final ClientRepository clientRepository;
    private final UserRepository userRepository;
    private final UserProfileMapper clientMapper;
    private final FileStorageService fileStorageService;

    @Override
    public UserProfileResponseDto createProfile(UserProfileRequestDto clientDto, MultipartFile photoFile) throws IOException {
        User user = this.userRepository.findById(clientDto.getUserId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        String fileName = fileStorageService.saveFile(photoFile);

        UserProfile client = this.clientMapper.toEntity(clientDto, user, fileName);
        UserProfile clientSave = this.clientRepository.save(client);

        return clientMapper.toDto(clientSave);

    }

    @Override
    public List<UserProfileResponseDto> getAllProfiles() {
        return clientRepository.findAll()
                .stream()
                .map(clientMapper::toDto)
                .toList();
    }

    @Override
    public UserProfileResponseDto getProfileById(Long id) {
        UserProfile client = clientRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Customer not found"));

        return clientMapper.toDto(client);
    }

    @Override
    public UserProfileResponseDto getProfileByUser(Long id) {
        User user = this.userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found"));

        UserProfile client = clientRepository.findByUser(user);

        return clientMapper.toDto(client);
    }

    @Override
    public UserProfileResponseDto updateProfile(Long id, UserProfileRequestDto dto) {
        UserProfile client = clientRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Profile not found"));

        User user = userRepository.findById(dto.getUserId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        client.setLastName(dto.getLastName());
        client.setFirstName(dto.getFirstName());
        client.setPhone(dto.getPhone());
        client.setAddress(dto.getAddress());
        client.setCountry(dto.getCountry());
        client.setCity(dto.getCity());
        client.setBorough(dto.getBorough());
        client.setUser(user);

        return clientMapper.toDto(clientRepository.save(client));
    }

    @Override
    public UserProfileResponseDto updatePhotoProfile(Long id, MultipartFile photoFile) throws IOException {

        UserProfile profile = clientRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Profile not found"));

        if (photoFile != null && !photoFile.isEmpty()) {

            // supprimer ancien logo
            if (profile.getPhoto() != null) {
                Path oldPath = Paths.get("uploads/" + profile.getPhoto());
                Files.deleteIfExists(oldPath);
            }

            // utiliser FileStorageService
            String fileName = fileStorageService.saveFile(photoFile);
            profile.setPhoto(fileName);
        }

        UserProfile updated = clientRepository.save(profile);

        return clientMapper.toDto(clientRepository.save(updated));
    }

    @Override
    public void deleteProfile(Long id) {
        UserProfile client = clientRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Customer not found"));

        clientRepository.delete(client);
    }


}
